"""Academic and web source retrieval for real citations.

Searches OpenAlex, arXiv, Semantic Scholar, Brave, PubMed, Europe PMC,
CORE, and CrossRef to gather real references before manuscript writing.
Key-less APIs (OpenAlex, arXiv, PubMed, Europe PMC, CrossRef) work
immediately; key-gated APIs activate when env vars are set.
"""

import asyncio
import logging
import os
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

import aiohttp

from ..models.collaborative_research import Reference
from .normalize_ref import normalize_title, clean_doi


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

@dataclass
class _RateLimiter:
    """Token-bucket style per-API rate limiter."""

    interval: float  # minimum seconds between requests
    _last: float = field(default=0.0, repr=False)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, repr=False)

    async def wait(self):
        async with self._lock:
            now = time.monotonic()
            delay = self.interval - (now - self._last)
            if delay > 0:
                await asyncio.sleep(delay)
            self._last = time.monotonic()


# ---------------------------------------------------------------------------
# In-memory cache with TTL
# ---------------------------------------------------------------------------

@dataclass
class _CacheEntry:
    data: List[Reference]
    expires: float


class _TTLCache:
    """Simple in-memory cache with per-key TTL."""

    def __init__(self, ttl: float = 1800.0):  # 30 min default
        self._store: Dict[str, _CacheEntry] = {}
        self._ttl = ttl

    def get(self, key: str) -> Optional[List[Reference]]:
        entry = self._store.get(key)
        if entry is None:
            return None
        if time.monotonic() > entry.expires:
            del self._store[key]
            return None
        return entry.data

    def put(self, key: str, data: List[Reference]):
        self._store[key] = _CacheEntry(data=data, expires=time.monotonic() + self._ttl)


# ---------------------------------------------------------------------------
# SourceRetriever
# ---------------------------------------------------------------------------

class SourceRetriever:
    """Searches academic databases and the web for real references.

    Key-less APIs (OpenAlex, arXiv, PubMed, Europe PMC, CrossRef) always work.
    Key-gated APIs activate automatically when env vars are set:
      - SEMANTIC_SCHOLAR_API_KEY
      - BRAVE_API_KEY
      - CORE_API_KEY  (optional, enables CORE API)
    """

    _HEADERS = {
        "User-Agent": "AutonomousResearchPress/1.0 (research bot)",
        "Accept-Encoding": "gzip, deflate",
    }

    # Domain → API combination mapping
    _DOMAIN_APIS: Dict[str, List[str]] = {
        "medicine_health": ["openalex", "pubmed", "europe_pmc", "semantic_scholar", "brave"],
        "natural_sciences:biology": ["openalex", "pubmed", "arxiv", "semantic_scholar", "brave"],
        "natural_sciences": ["openalex", "arxiv", "semantic_scholar", "crossref", "brave"],
        "social_sciences": ["openalex", "core", "semantic_scholar", "crossref", "brave"],
        "humanities": ["openalex", "core", "crossref", "brave"],
        "business_economics": ["openalex", "core", "semantic_scholar", "crossref", "brave"],
        "law_policy": ["openalex", "core", "crossref", "brave"],
        "computer_science": ["openalex", "arxiv", "semantic_scholar", "brave"],
        "engineering": ["openalex", "arxiv", "semantic_scholar", "crossref", "brave"],
    }

    def __init__(self):
        self._cache = _TTLCache()
        self._limiters = {
            "openalex": _RateLimiter(interval=0.1),         # 10 req/s
            "arxiv": _RateLimiter(interval=3.0),             # 1 req/3s (arxiv ToS)
            "semantic_scholar": _RateLimiter(interval=1.0),  # 1 req/s
            "brave": _RateLimiter(interval=1.0),             # 1 req/s
            "pubmed": _RateLimiter(interval=0.35),           # ~3 req/s (no key)
            "europe_pmc": _RateLimiter(interval=0.5),        # conservative
            "core": _RateLimiter(interval=6.0),              # 10 req/min
            "crossref": _RateLimiter(interval=0.1),          # 50 req/s (polite pool)
        }

    # ------------------------------------------------------------------
    # OpenAlex  (free, no key)
    # ------------------------------------------------------------------

    async def search_openalex(self, query: str, max_results: int = 5) -> List[Reference]:
        cache_key = f"openalex:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["openalex"].wait()

        url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per_page": max_results,
            "sort": "relevance_score:desc",
            "select": "id,title,authorships,primary_location,publication_year,doi",
        }

        refs: List[Reference] = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=self._HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    data = await resp.json()

            for i, work in enumerate(data.get("results", []), start=1):
                authors = []
                for authorship in work.get("authorships", [])[:5]:
                    name = authorship.get("author", {}).get("display_name")
                    if name:
                        authors.append(name)

                venue = ""
                loc = work.get("primary_location") or {}
                source = loc.get("source") or {}
                venue = source.get("display_name", "")

                doi_raw = work.get("doi") or ""
                doi = doi_raw.replace("https://doi.org/", "") if doi_raw else None

                refs.append(Reference(
                    id=0,  # assigned later during dedup
                    authors=authors or ["Unknown"],
                    title=work.get("title") or "Untitled",
                    venue=venue or "OpenAlex",
                    year=work.get("publication_year") or 0,
                    url=doi_raw or None,
                    doi=doi,
                    summary="",
                ))
        except Exception:
            pass

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # arXiv  (free, no key)
    # ------------------------------------------------------------------

    async def search_arxiv(self, query: str, max_results: int = 5) -> List[Reference]:
        cache_key = f"arxiv:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["arxiv"].wait()

        url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        refs: List[Reference] = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=self._HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    text = await resp.text()

            ns = {"atom": "http://www.w3.org/2005/Atom"}
            root = ET.fromstring(text)

            for entry in root.findall("atom:entry", ns):
                title_el = entry.find("atom:title", ns)
                title = title_el.text.strip().replace("\n", " ") if title_el is not None and title_el.text else "Untitled"

                authors = []
                for author_el in entry.findall("atom:author", ns):
                    name_el = author_el.find("atom:name", ns)
                    if name_el is not None and name_el.text:
                        authors.append(name_el.text.strip())

                published = entry.find("atom:published", ns)
                year = 0
                if published is not None and published.text:
                    year = int(published.text[:4])

                link_el = entry.find("atom:id", ns)
                arxiv_url = link_el.text.strip() if link_el is not None and link_el.text else None

                # Extract arXiv ID for DOI-like reference
                arxiv_id = None
                if arxiv_url:
                    match = re.search(r"(\d{4}\.\d{4,5})", arxiv_url)
                    if match:
                        arxiv_id = match.group(1)

                refs.append(Reference(
                    id=0,
                    authors=authors or ["Unknown"],
                    title=title,
                    venue="arXiv",
                    year=year,
                    url=arxiv_url,
                    doi=f"arXiv:{arxiv_id}" if arxiv_id else None,
                    summary="",
                ))
        except Exception:
            pass

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # Semantic Scholar  (key optional, higher rate limit with key)
    # ------------------------------------------------------------------

    async def search_semantic_scholar(self, query: str, max_results: int = 5) -> List[Reference]:
        api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        if not api_key:
            return []

        cache_key = f"ss:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["semantic_scholar"].wait()

        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,year,venue,externalIds,url",
        }
        headers = {**self._HEADERS, "x-api-key": api_key}

        refs: List[Reference] = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    data = await resp.json()

            for paper in data.get("data", []):
                authors = [a.get("name", "Unknown") for a in paper.get("authors", [])[:5]]
                ext_ids = paper.get("externalIds") or {}
                doi = ext_ids.get("DOI")

                refs.append(Reference(
                    id=0,
                    authors=authors or ["Unknown"],
                    title=paper.get("title") or "Untitled",
                    venue=paper.get("venue") or "Semantic Scholar",
                    year=paper.get("year") or 0,
                    url=paper.get("url"),
                    doi=doi,
                    summary="",
                ))
        except Exception:
            pass

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # PubMed / NCBI E-utilities  (free, no key required)
    # ------------------------------------------------------------------

    async def search_pubmed(self, query: str, max_results: int = 5) -> List[Reference]:
        cache_key = f"pubmed:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["pubmed"].wait()

        refs: List[Reference] = []
        try:
            # Step 1: esearch to get PMIDs
            esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            esearch_params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "sort": "relevance",
                "retmode": "json",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(esearch_url, params=esearch_params, headers=self._HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    data = await resp.json()

            id_list = data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                return refs

            # Step 2: efetch to get article details
            await self._limiters["pubmed"].wait()
            efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            efetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "xml",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(efetch_url, params=efetch_params, headers=self._HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    text = await resp.text()

            root = ET.fromstring(text)
            for article in root.findall(".//PubmedArticle"):
                medline = article.find(".//MedlineCitation")
                if medline is None:
                    continue

                # Title
                title_el = medline.find(".//ArticleTitle")
                title = title_el.text.strip() if title_el is not None and title_el.text else "Untitled"

                # Authors
                authors = []
                for author_el in medline.findall(".//Author")[:5]:
                    last = author_el.findtext("LastName", "")
                    fore = author_el.findtext("ForeName", "")
                    if last:
                        authors.append(f"{last} {fore}".strip())

                # Year
                year = 0
                year_el = medline.find(".//PubDate/Year")
                if year_el is not None and year_el.text:
                    year = int(year_el.text)

                # Journal
                journal_el = medline.find(".//Journal/Title")
                venue = journal_el.text if journal_el is not None and journal_el.text else "PubMed"

                # PMID → URL and DOI
                pmid_el = medline.find("PMID")
                pmid = pmid_el.text if pmid_el is not None and pmid_el.text else None
                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None

                doi = None
                for id_el in article.findall(".//ArticleId"):
                    if id_el.get("IdType") == "doi" and id_el.text:
                        doi = id_el.text.strip()
                        break

                refs.append(Reference(
                    id=0,
                    authors=authors or ["Unknown"],
                    title=title,
                    venue=venue,
                    year=year,
                    url=url,
                    doi=doi,
                    summary="",
                ))
        except Exception as e:
            logger.warning(f"PubMed search failed: {e}")

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # Europe PMC  (free, no key required)
    # ------------------------------------------------------------------

    async def search_europe_pmc(self, query: str, max_results: int = 5) -> List[Reference]:
        cache_key = f"europepmc:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["europe_pmc"].wait()

        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        params = {
            "query": query,
            "format": "json",
            "pageSize": max_results,
            "sort": "RELEVANCE",
            "resultType": "core",
        }

        refs: List[Reference] = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=self._HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    data = await resp.json()

            for result in data.get("resultList", {}).get("result", []):
                authors = []
                for author_info in (result.get("authorList", {}).get("author", []) or [])[:5]:
                    name = author_info.get("fullName")
                    if name:
                        authors.append(name)

                doi = result.get("doi")
                pmid = result.get("pmid")
                result_url = None
                if doi:
                    result_url = f"https://doi.org/{doi}"
                elif pmid:
                    result_url = f"https://europepmc.org/article/MED/{pmid}"

                year = 0
                pub_year = result.get("pubYear")
                if pub_year:
                    try:
                        year = int(pub_year)
                    except (ValueError, TypeError):
                        pass

                refs.append(Reference(
                    id=0,
                    authors=authors or ["Unknown"],
                    title=result.get("title", "Untitled").strip(),
                    venue=result.get("journalTitle") or "Europe PMC",
                    year=year,
                    url=result_url,
                    doi=doi,
                    summary="",
                ))
        except Exception as e:
            logger.warning(f"Europe PMC search failed: {e}")

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # CORE  (key required via CORE_API_KEY env var)
    # ------------------------------------------------------------------

    async def search_core(self, query: str, max_results: int = 5) -> List[Reference]:
        api_key = os.environ.get("CORE_API_KEY")
        if not api_key:
            return []

        cache_key = f"core:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["core"].wait()

        url = "https://api.core.ac.uk/v3/search/works"
        params = {"q": query, "limit": max_results}
        headers = {**self._HEADERS, "Authorization": f"Bearer {api_key}"}

        refs: List[Reference] = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    data = await resp.json()

            for result in data.get("results", []):
                authors = []
                for author_info in (result.get("authors") or [])[:5]:
                    name = author_info.get("name")
                    if name:
                        authors.append(name)

                doi = None
                for ident in result.get("identifiers") or []:
                    if isinstance(ident, str) and ident.startswith("10."):
                        doi = ident
                        break

                year = 0
                pub_year = result.get("yearPublished")
                if pub_year:
                    try:
                        year = int(pub_year)
                    except (ValueError, TypeError):
                        pass

                result_url = None
                for link in result.get("links") or []:
                    if isinstance(link, dict) and link.get("url"):
                        result_url = link["url"]
                        break
                if not result_url and doi:
                    result_url = f"https://doi.org/{doi}"

                refs.append(Reference(
                    id=0,
                    authors=authors or ["Unknown"],
                    title=result.get("title", "Untitled").strip(),
                    venue=result.get("publisher") or "CORE",
                    year=year,
                    url=result_url,
                    doi=doi,
                    summary="",
                ))
        except Exception as e:
            logger.warning(f"CORE search failed: {e}")

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # CrossRef  (free, polite pool via mailto in User-Agent)
    # ------------------------------------------------------------------

    async def search_crossref(self, query: str, max_results: int = 5) -> List[Reference]:
        cache_key = f"crossref:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["crossref"].wait()

        url = "https://api.crossref.org/works"
        params = {
            "query": query,
            "rows": max_results,
            "sort": "relevance",
            "select": "DOI,title,author,container-title,published-print,published-online,URL",
        }
        headers = {
            **self._HEADERS,
            "User-Agent": "AutonomousResearchPress/1.0 (mailto:research@autonomouspress.dev)",
        }

        refs: List[Reference] = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    data = await resp.json()

            for item in data.get("message", {}).get("items", []):
                authors = []
                for author_info in (item.get("author") or [])[:5]:
                    given = author_info.get("given", "")
                    family = author_info.get("family", "")
                    name = f"{family} {given}".strip()
                    if name:
                        authors.append(name)

                titles = item.get("title") or []
                title = titles[0] if titles else "Untitled"

                venues = item.get("container-title") or []
                venue = venues[0] if venues else "CrossRef"

                doi = item.get("DOI")
                result_url = item.get("URL") or (f"https://doi.org/{doi}" if doi else None)

                year = 0
                for date_key in ("published-print", "published-online"):
                    date_parts = (item.get(date_key) or {}).get("date-parts", [[]])
                    if date_parts and date_parts[0]:
                        try:
                            year = int(date_parts[0][0])
                            break
                        except (ValueError, TypeError, IndexError):
                            pass

                refs.append(Reference(
                    id=0,
                    authors=authors or ["Unknown"],
                    title=title.strip() if isinstance(title, str) else "Untitled",
                    venue=venue,
                    year=year,
                    url=result_url,
                    doi=doi,
                    summary="",
                ))
        except Exception as e:
            logger.warning(f"CrossRef search failed: {e}")

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # Brave Search  (key required, 2000 free/month)
    # ------------------------------------------------------------------

    async def search_brave(self, query: str, max_results: int = 4) -> List[Reference]:
        api_key = os.environ.get("BRAVE_API_KEY")
        if not api_key:
            return []

        cache_key = f"brave:{query}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        await self._limiters["brave"].wait()

        url = "https://api.search.brave.com/res/v1/web/search"
        params = {"q": query, "count": max_results}
        headers = {
            **self._HEADERS,
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key,
        }

        refs: List[Reference] = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return refs
                    data = await resp.json()

            for result in data.get("web", {}).get("results", []):
                title = result.get("title", "Untitled")
                page_url = result.get("url", "")
                description = result.get("description", "")

                refs.append(Reference(
                    id=0,
                    authors=["Web Source"],
                    title=title,
                    venue=page_url.split("/")[2] if "/" in page_url else "Web",
                    year=0,
                    url=page_url,
                    doi=None,
                    summary=description[:200],
                ))
        except Exception:
            pass

        self._cache.put(cache_key, refs)
        return refs

    # ------------------------------------------------------------------
    # Unified search
    # ------------------------------------------------------------------

    def _select_apis(self, category: Optional[dict] = None) -> List[str]:
        """Select which APIs to query based on the academic domain.

        Args:
            category: Optional dict with 'major' and optionally 'subfield' keys

        Returns:
            List of API identifiers (method name suffixes)
        """
        if not category or not category.get("major"):
            # Default: original set
            return ["openalex", "arxiv", "semantic_scholar", "brave"]

        major = category["major"]
        subfield = (category.get("subfield") or "").lower()

        # Check subfield-specific mapping first (e.g. natural_sciences:biology)
        key_with_sub = f"{major}:{subfield}"
        if key_with_sub in self._DOMAIN_APIS:
            apis = list(self._DOMAIN_APIS[key_with_sub])
        elif major in self._DOMAIN_APIS:
            apis = list(self._DOMAIN_APIS[major])
        else:
            apis = ["openalex", "arxiv", "semantic_scholar", "brave"]

        # Also include secondary domain APIs if present
        secondary = category.get("secondary_major")
        if secondary and secondary in self._DOMAIN_APIS:
            for api in self._DOMAIN_APIS[secondary]:
                if api not in apis:
                    apis.append(api)

        return apis

    async def search_all(
        self,
        topic: str,
        max_academic: int = 15,
        max_web: int = 4,
        category: Optional[dict] = None,
    ) -> List[Reference]:
        """Search domain-appropriate sources, deduplicate, and assign IDs.

        Args:
            topic: Research topic string
            max_academic: Max academic results (split across sources)
            max_web: Max web results from Brave
            category: Optional dict with 'major' and 'subfield' for domain-aware
                API selection

        Returns:
            Deduplicated list of References with sequential IDs starting at 1
        """
        selected_apis = self._select_apis(category)

        # Count academic APIs (everything except 'brave')
        academic_apis = [a for a in selected_apis if a != "brave"]
        per_academic = max(2, max_academic // max(len(academic_apis), 1))

        # Build coroutines based on selected APIs
        _api_methods = {
            "openalex": lambda: self.search_openalex(topic, max_results=per_academic),
            "arxiv": lambda: self.search_arxiv(topic, max_results=per_academic),
            "semantic_scholar": lambda: self.search_semantic_scholar(topic, max_results=per_academic),
            "brave": lambda: self.search_brave(topic, max_results=max_web),
            "pubmed": lambda: self.search_pubmed(topic, max_results=per_academic),
            "europe_pmc": lambda: self.search_europe_pmc(topic, max_results=per_academic),
            "core": lambda: self.search_core(topic, max_results=per_academic),
            "crossref": lambda: self.search_crossref(topic, max_results=per_academic),
        }

        coros = []
        for api_name in selected_apis:
            factory = _api_methods.get(api_name)
            if factory:
                coros.append(factory())

        # Launch all searches concurrently
        results = await asyncio.gather(*coros, return_exceptions=True)

        all_refs: List[Reference] = []
        for result in results:
            if isinstance(result, list):
                all_refs.extend(result)

        # Deduplicate: DOI first, then normalized title
        seen_dois: set = set()
        seen_titles: set = set()
        unique_refs: List[Reference] = []
        for ref in all_refs:
            # Clean bogus DOIs before comparison
            ref.doi = clean_doi(ref.doi)

            # Skip untitled
            norm = normalize_title(ref.title)
            if not norm or norm == "untitled":
                continue

            # DOI-based dedup (strongest signal)
            if ref.doi:
                doi_key = ref.doi.lower().strip()
                if doi_key in seen_dois:
                    continue
                seen_dois.add(doi_key)

            # Title-based dedup (fallback)
            if norm in seen_titles:
                continue
            seen_titles.add(norm)
            unique_refs.append(ref)

        # Assign sequential IDs
        for i, ref in enumerate(unique_refs, start=1):
            ref.id = i

        return unique_refs

    # ------------------------------------------------------------------
    # Formatting helper (for prompt injection)
    # ------------------------------------------------------------------

    @staticmethod
    def format_for_prompt(references: List[Reference]) -> str:
        """Format references into a text block suitable for LLM prompts.

        Example output:
          [1] Smith, Lee (2023). "Title". Venue. https://doi.org/10.xxx
          [2] ...
        """
        if not references:
            return ""

        lines = []
        for ref in references:
            authors = ", ".join(ref.authors[:3])
            if len(ref.authors) > 3:
                authors += " et al."

            line = f"[{ref.id}] {authors} ({ref.year}). \"{ref.title}\". {ref.venue}."
            if ref.doi and not ref.doi.startswith("arXiv:"):
                line += f" https://doi.org/{ref.doi}"
            elif ref.url:
                line += f" {ref.url}"
            lines.append(line)

        return "\n".join(lines)
