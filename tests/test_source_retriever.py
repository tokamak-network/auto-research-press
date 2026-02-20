"""Tests for source_retriever: new API methods, domain selection, and ghost citation stripping."""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from research_cli.models.collaborative_research import Reference
from research_cli.utils.source_retriever import SourceRetriever
from research_cli.workflow.orchestrator import _strip_ghost_citations


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(coro):
    """Run an async coroutine synchronously for tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


def _make_ref(id: int, title: str, doi: str | None = None, year: int = 2023) -> Reference:
    return Reference(
        id=id,
        authors=["Author A"],
        title=title,
        venue="Test Journal",
        year=year,
        url=f"https://example.com/{id}",
        doi=doi,
        summary="",
    )


def _make_aiohttp_response(status: int, payload: dict | str):
    """Return a mock aiohttp response context manager."""
    resp = AsyncMock()
    resp.status = status
    if isinstance(payload, str):
        resp.text = AsyncMock(return_value=payload)
        resp.json = AsyncMock(side_effect=Exception("not json"))
    else:
        resp.json = AsyncMock(return_value=payload)
        resp.text = AsyncMock(return_value=json.dumps(payload))

    ctx = AsyncMock()
    ctx.__aenter__ = AsyncMock(return_value=resp)
    ctx.__aiter__ = AsyncMock(return_value=iter([]))
    ctx.__aexit__ = AsyncMock(return_value=False)
    return ctx


class _FakeSession:
    """Minimal fake for aiohttp.ClientSession that returns canned responses."""

    def __init__(self, response_ctx):
        self._response_ctx = response_ctx

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def get(self, *args, **kwargs):
        return self._response_ctx


# ---------------------------------------------------------------------------
# _select_apis domain routing tests
# ---------------------------------------------------------------------------

class TestSelectApis:
    def setup_method(self):
        self.retriever = SourceRetriever()

    def test_no_category_returns_defaults(self):
        apis = self.retriever._select_apis(None)
        assert "openalex" in apis
        assert "arxiv" in apis

    def test_computer_science_no_pubmed(self):
        apis = self.retriever._select_apis({"major": "computer_science", "subfield": "ai"})
        assert "openalex" in apis
        assert "arxiv" in apis
        assert "pubmed" not in apis

    def test_medicine_includes_pubmed_and_europe_pmc(self):
        apis = self.retriever._select_apis({"major": "medicine_health", "subfield": "oncology"})
        assert "pubmed" in apis
        assert "europe_pmc" in apis
        assert "arxiv" not in apis

    def test_natural_sciences_biology_includes_pubmed(self):
        apis = self.retriever._select_apis({"major": "natural_sciences", "subfield": "biology"})
        assert "pubmed" in apis
        assert "arxiv" in apis

    def test_natural_sciences_physics_no_pubmed(self):
        apis = self.retriever._select_apis({"major": "natural_sciences", "subfield": "physics"})
        assert "pubmed" not in apis
        assert "crossref" in apis

    def test_social_sciences_includes_core(self):
        apis = self.retriever._select_apis({"major": "social_sciences", "subfield": "sociology"})
        assert "core" in apis
        assert "crossref" in apis

    def test_humanities_includes_core(self):
        apis = self.retriever._select_apis({"major": "humanities", "subfield": "history"})
        assert "core" in apis
        assert "crossref" in apis
        assert "arxiv" not in apis

    def test_secondary_major_adds_apis(self):
        apis = self.retriever._select_apis({
            "major": "computer_science",
            "subfield": "ai",
            "secondary_major": "medicine_health",
        })
        assert "pubmed" in apis  # from secondary
        assert "arxiv" in apis   # from primary

    def test_unknown_major_returns_defaults(self):
        apis = self.retriever._select_apis({"major": "unknown_field"})
        assert "openalex" in apis
        assert "arxiv" in apis


# ---------------------------------------------------------------------------
# _strip_ghost_citations tests
# ---------------------------------------------------------------------------

class TestStripGhostCitations:
    def test_no_refs_section_returns_unchanged(self):
        manuscript = "Some text without references."
        refs = [_make_ref(1, "Real Paper")]
        assert _strip_ghost_citations(manuscript, refs) == manuscript

    def test_empty_verified_refs_returns_unchanged(self):
        manuscript = "Body\n\n## References\n\n[1] Fake Paper"
        assert _strip_ghost_citations(manuscript, []) == manuscript

    def test_keeps_verified_ref_by_title(self):
        verified = [_make_ref(1, "Real Paper on CRISPR")]
        manuscript = (
            'Body text [1] and [2] here.\n\n'
            '## References\n\n'
            '[1] Author A (2023). "Real Paper on CRISPR". Journal.\n'
            '[2] Author B (2023). "Fabricated Citation". Fake Journal.'
        )
        result = _strip_ghost_citations(manuscript, verified)
        assert "[1]" in result
        assert "Real Paper on CRISPR" in result
        assert "Fabricated Citation" not in result
        # Ghost inline citation [2] should be removed from body
        assert "[2]" not in result

    def test_keeps_verified_ref_by_doi(self):
        verified = [_make_ref(1, "Paper Title", doi="10.1234/test.2023")]
        manuscript = (
            'Body [1] and [2].\n\n'
            '## References\n\n'
            '[1] Author (2023). "Different Title". J. doi: 10.1234/test.2023\n'
            '[2] Author (2023). "Ghost Paper". Fake.'
        )
        result = _strip_ghost_citations(manuscript, verified)
        assert "10.1234/test.2023" in result
        assert "Ghost Paper" not in result

    def test_renumbers_citations_sequentially(self):
        verified = [
            _make_ref(1, "Paper Alpha"),
            _make_ref(2, "Paper Gamma"),
        ]
        manuscript = (
            'Body cites [1], [2], [3].\n\n'
            '## References\n\n'
            '[1] Author (2023). "Paper Alpha". J.\n'
            '[2] Author (2023). "Ghost Paper". Fake.\n'
            '[3] Author (2023). "Paper Gamma". J.'
        )
        result = _strip_ghost_citations(manuscript, verified)
        # [1] stays [1], [3] becomes [2], [2] (ghost) removed
        assert "Body cites [1]," in result
        assert "[2]" in result  # renumbered from [3]
        assert "Paper Gamma" in result
        assert "Ghost Paper" not in result

    def test_all_verified_no_change(self):
        verified = [
            _make_ref(1, "Paper A"),
            _make_ref(2, "Paper B"),
        ]
        manuscript = (
            'Body [1] [2].\n\n'
            '## References\n\n'
            '[1] Author (2023). "Paper A". J.\n'
            '[2] Author (2023). "Paper B". J.'
        )
        result = _strip_ghost_citations(manuscript, verified)
        assert "Paper A" in result
        assert "Paper B" in result

    def test_handles_hash_references_heading(self):
        """Handle ## References and ### References headings."""
        verified = [_make_ref(1, "Real Paper")]
        manuscript = (
            'Body [1] [2].\n\n'
            '### References\n\n'
            '[1] Author (2023). "Real Paper". J.\n'
            '[2] Author (2023). "Ghost". Fake.'
        )
        result = _strip_ghost_citations(manuscript, verified)
        assert "Real Paper" in result
        assert "Ghost" not in result


# ---------------------------------------------------------------------------
# Individual API method tests (mocked HTTP)
# ---------------------------------------------------------------------------

class TestSearchPubmed:
    def test_pubmed_parses_xml(self):
        retriever = SourceRetriever()

        esearch_response = {
            "esearchresult": {"idlist": ["12345"]}
        }

        efetch_xml = """<?xml version="1.0"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345</PMID>
      <Article>
        <ArticleTitle>CRISPR Gene Editing in Cancer</ArticleTitle>
        <AuthorList>
          <Author><LastName>Smith</LastName><ForeName>John</ForeName></Author>
        </AuthorList>
        <Journal><Title>Nature Medicine</Title></Journal>
      </Article>
      <DateCompleted><Year>2023</Year></DateCompleted>
    </MedlineCitation>
    <PubmedData>
      <ArticleIdList>
        <ArticleId IdType="doi">10.1038/nm.2023</ArticleId>
      </ArticleIdList>
    </PubmedData>
  </PubmedArticle>
</PubmedArticleSet>"""

        call_count = 0
        def fake_get(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 1:
                return _make_aiohttp_response(200, esearch_response)
            else:
                return _make_aiohttp_response(200, efetch_xml)

        fake_session = MagicMock()
        fake_session.__aenter__ = AsyncMock(return_value=fake_session)
        fake_session.__aexit__ = AsyncMock(return_value=False)
        fake_session.get = fake_get

        with patch("aiohttp.ClientSession", return_value=fake_session):
            refs = _run(retriever.search_pubmed("CRISPR cancer"))

        assert len(refs) == 1
        assert refs[0].title == "CRISPR Gene Editing in Cancer"
        assert refs[0].doi == "10.1038/nm.2023"

    def test_pubmed_failure_returns_empty(self):
        retriever = SourceRetriever()

        with patch("aiohttp.ClientSession", side_effect=Exception("network error")):
            refs = _run(retriever.search_pubmed("test query"))

        assert refs == []


class TestSearchEuropePmc:
    def test_europe_pmc_parses_json(self):
        retriever = SourceRetriever()

        api_response = {
            "resultList": {
                "result": [{
                    "title": "Immunotherapy Advances",
                    "authorList": {"author": [{"fullName": "Jane Doe"}]},
                    "journalTitle": "The Lancet",
                    "pubYear": "2023",
                    "doi": "10.1016/lancet.2023",
                    "pmid": "99999",
                }]
            }
        }

        fake_session = _FakeSession(_make_aiohttp_response(200, api_response))
        with patch("aiohttp.ClientSession", return_value=fake_session):
            refs = _run(retriever.search_europe_pmc("immunotherapy"))

        assert len(refs) == 1
        assert refs[0].title == "Immunotherapy Advances"
        assert refs[0].doi == "10.1016/lancet.2023"


class TestSearchCore:
    def test_core_requires_api_key(self):
        retriever = SourceRetriever()
        with patch.dict("os.environ", {}, clear=True):
            refs = _run(retriever.search_core("test"))
        assert refs == []

    def test_core_parses_results(self):
        retriever = SourceRetriever()

        api_response = {
            "results": [{
                "title": "Digital Humanities Methods",
                "authors": [{"name": "Alice"}],
                "yearPublished": 2022,
                "identifiers": ["10.5555/dh.2022"],
                "links": [{"url": "https://example.com/dh"}],
                "publisher": "Oxford University Press",
            }]
        }

        fake_session = _FakeSession(_make_aiohttp_response(200, api_response))
        with patch("aiohttp.ClientSession", return_value=fake_session):
            with patch.dict("os.environ", {"CORE_API_KEY": "test-key"}):
                refs = _run(retriever.search_core("digital humanities"))

        assert len(refs) == 1
        assert refs[0].title == "Digital Humanities Methods"
        assert refs[0].doi == "10.5555/dh.2022"


class TestSearchCrossref:
    def test_crossref_parses_items(self):
        retriever = SourceRetriever()

        api_response = {
            "message": {
                "items": [{
                    "title": ["Quantum Computing Survey"],
                    "author": [{"given": "Bob", "family": "Smith"}],
                    "container-title": ["Physical Review Letters"],
                    "DOI": "10.1103/prl.2023",
                    "URL": "https://doi.org/10.1103/prl.2023",
                    "published-print": {"date-parts": [[2023]]},
                }]
            }
        }

        fake_session = _FakeSession(_make_aiohttp_response(200, api_response))
        with patch("aiohttp.ClientSession", return_value=fake_session):
            refs = _run(retriever.search_crossref("quantum computing"))

        assert len(refs) == 1
        assert refs[0].title == "Quantum Computing Survey"
        assert refs[0].doi == "10.1103/prl.2023"
        assert refs[0].year == 2023

    def test_crossref_failure_returns_empty(self):
        retriever = SourceRetriever()

        with patch("aiohttp.ClientSession", side_effect=Exception("timeout")):
            refs = _run(retriever.search_crossref("test"))

        assert refs == []


# ---------------------------------------------------------------------------
# search_all domain-based API selection integration test
# ---------------------------------------------------------------------------

class TestSearchAllDomain:
    def test_medicine_calls_pubmed(self):
        retriever = SourceRetriever()

        retriever.search_openalex = AsyncMock(return_value=[])
        retriever.search_pubmed = AsyncMock(return_value=[
            _make_ref(0, "PubMed Result", doi="10.1234/pm")
        ])
        retriever.search_europe_pmc = AsyncMock(return_value=[])
        retriever.search_semantic_scholar = AsyncMock(return_value=[])
        retriever.search_brave = AsyncMock(return_value=[])

        refs = _run(retriever.search_all(
            "cancer treatment",
            category={"major": "medicine_health", "subfield": "oncology"},
        ))

        retriever.search_pubmed.assert_called_once()
        retriever.search_europe_pmc.assert_called_once()

    def test_cs_does_not_call_pubmed(self):
        retriever = SourceRetriever()

        retriever.search_openalex = AsyncMock(return_value=[])
        retriever.search_arxiv = AsyncMock(return_value=[])
        retriever.search_semantic_scholar = AsyncMock(return_value=[])
        retriever.search_brave = AsyncMock(return_value=[])
        retriever.search_pubmed = AsyncMock(return_value=[])

        refs = _run(retriever.search_all(
            "machine learning",
            category={"major": "computer_science", "subfield": "ai"},
        ))

        retriever.search_pubmed.assert_not_called()
        retriever.search_arxiv.assert_called_once()

    def test_no_category_uses_defaults(self):
        retriever = SourceRetriever()

        retriever.search_openalex = AsyncMock(return_value=[])
        retriever.search_arxiv = AsyncMock(return_value=[])
        retriever.search_semantic_scholar = AsyncMock(return_value=[])
        retriever.search_brave = AsyncMock(return_value=[])

        refs = _run(retriever.search_all("test topic"))

        retriever.search_openalex.assert_called_once()
        retriever.search_arxiv.assert_called_once()
