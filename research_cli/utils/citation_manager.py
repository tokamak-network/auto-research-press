"""Citation management system with numbered citations and hyperlinks."""

import re
from typing import List, Dict, Tuple
from ..models.collaborative_research import Reference


class CitationManager:
    """
    Manages numbered citations with hyperlinks.

    Converts inline citations like [1], [2,3] into hyperlinked references.
    """

    @staticmethod
    def format_inline_citation(ref_ids: List[int]) -> str:
        """Format citation as [1,2,3]."""
        return f"[{','.join(map(str, ref_ids))}]"

    @staticmethod
    def extract_citations(text: str) -> List[int]:
        """Extract all citation numbers from text."""
        citations = set()
        pattern = r'\[(\d+(?:,\d+)*)\]'
        matches = re.findall(pattern, text)

        for match in matches:
            nums = match.split(',')
            for num in nums:
                try:
                    citations.add(int(num.strip()))
                except ValueError:
                    continue

        return sorted(list(citations))

    @staticmethod
    def add_citation_hyperlinks(text: str) -> str:
        """
        Convert inline citations to hyperlinks.

        [1] → <a href="#ref-1" class="citation-link">[1]</a>
        [1,2,3] → <a href="#ref-1">[1]</a>,<a href="#ref-2">[2]</a>,<a href="#ref-3">[3]</a>
        """
        def replace_citation(match):
            nums = match.group(1).split(',')
            links = []
            for num in nums:
                num = num.strip()
                links.append(f'<a href="#ref-{num}" class="citation-link" onclick="highlightReference({num})">[{num}]</a>')

            return '<span class="citation-group">' + ','.join(links) + '</span>'

        pattern = r'\[(\d+(?:,\d+)*)\]'
        return re.sub(pattern, replace_citation, text)

    @staticmethod
    def format_references_section(references: List[Reference]) -> str:
        """
        Format references section with IDs for hyperlinking.

        IEEE style with hyperlinks.
        """
        lines = ["## References\n"]

        for ref in sorted(references, key=lambda r: r.id):
            # Format authors
            authors = ", ".join(ref.authors[:3])
            if len(ref.authors) > 3:
                authors += " et al."

            # Main citation
            ref_text = f'<div id="ref-{ref.id}" class="reference-entry" data-ref-id="{ref.id}">\n'
            ref_text += f'[{ref.id}] {authors} ({ref.year}). "{ref.title}". *{ref.venue}*.'

            # Add URL/DOI
            if ref.url:
                ref_text += f'\n<br>&nbsp;&nbsp;&nbsp;&nbsp;Available: [{ref.url}]({ref.url})'
            if ref.doi:
                ref_text += f'\n<br>&nbsp;&nbsp;&nbsp;&nbsp;DOI: [{ref.doi}](https://doi.org/{ref.doi})'

            ref_text += '\n</div>\n'
            lines.append(ref_text)

        return "\n".join(lines)

    @staticmethod
    def format_references_markdown(references: List[Reference]) -> str:
        """
        Format references section as plain markdown (for .md files).
        """
        lines = ["## References\n"]

        for ref in sorted(references, key=lambda r: r.id):
            authors = ", ".join(ref.authors[:3])
            if len(ref.authors) > 3:
                authors += " et al."

            ref_text = f'[{ref.id}] {authors} ({ref.year}). "{ref.title}". {ref.venue}.'

            if ref.url:
                ref_text += f'\n    Available: {ref.url}'
            if ref.doi:
                ref_text += f'\n    DOI: https://doi.org/{ref.doi}'

            lines.append(ref_text + "\n")

        return "\n".join(lines)

    @staticmethod
    def validate_citations(text: str, references: List[Reference]) -> Tuple[bool, List[str]]:
        """
        Validate that all citations in text have corresponding references.

        Returns:
            (is_valid, list_of_errors)
        """
        cited_ids = CitationManager.extract_citations(text)
        ref_ids = {ref.id for ref in references}

        errors = []
        for cited_id in cited_ids:
            if cited_id not in ref_ids:
                errors.append(f"Citation [{cited_id}] has no corresponding reference")

        return len(errors) == 0, errors

    @staticmethod
    def get_citation_statistics(text: str, references: List[Reference]) -> Dict:
        """Get statistics about citations."""
        cited_ids = CitationManager.extract_citations(text)
        ref_ids = {ref.id for ref in references}

        unused_refs = ref_ids - set(cited_ids)

        return {
            "total_citations": len(cited_ids),
            "unique_citations": len(set(cited_ids)),
            "total_references": len(references),
            "unused_references": len(unused_refs),
            "unused_reference_ids": sorted(list(unused_refs))
        }


def convert_manuscript_to_html_with_citations(
    markdown_text: str,
    references: List[Reference]
) -> str:
    """
    Convert manuscript markdown to HTML with hyperlinked citations.

    Args:
        markdown_text: Markdown text with inline citations [1], [2]
        references: List of Reference objects

    Returns:
        HTML with hyperlinked citations and formatted references
    """
    # First convert markdown to HTML (using marked.js on frontend)
    # Here we just add citation hyperlinks to the markdown
    text_with_links = CitationManager.add_citation_hyperlinks(markdown_text)

    # Add references section
    refs_html = CitationManager.format_references_section(references)

    # Combine
    full_html = text_with_links + "\n\n---\n\n" + refs_html

    return full_html


# JavaScript code for web viewer (to be added to review.html)
CITATION_JAVASCRIPT = """
<script>
function highlightReference(refId) {
    // Remove previous highlights
    document.querySelectorAll('.reference-entry').forEach(el => {
        el.classList.remove('highlight-flash');
    });

    // Scroll to reference
    const refElement = document.getElementById(`ref-${refId}`);
    if (refElement) {
        refElement.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Highlight animation
        refElement.classList.add('highlight-flash');
        setTimeout(() => refElement.classList.remove('highlight-flash'), 2000);
    }
}

// Add click handlers to citation links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.citation-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const refId = this.getAttribute('href').replace('#ref-', '');
            highlightReference(parseInt(refId));
        });
    });
});
</script>
"""

CITATION_CSS = """
<style>
.citation-link {
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
    padding: 0 2px;
    transition: background-color 0.2s;
    cursor: pointer;
}

.citation-link:hover {
    background-color: #dbeafe;
    border-radius: 2px;
}

.citation-group {
    white-space: nowrap;
}

.reference-entry {
    padding: 0.75rem;
    margin: 0.5rem 0;
    border-left: 3px solid transparent;
    transition: all 0.3s;
}

.reference-entry.highlight-flash {
    background-color: #fef3c7;
    border-left-color: #f59e0b;
}

.reference-entry[data-ref-id] {
    scroll-margin-top: 80px; /* Account for fixed header */
}
</style>
"""
