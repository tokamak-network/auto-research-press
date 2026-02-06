"""Manuscript planning and section models."""

from dataclasses import dataclass, field
from typing import List, Optional, Literal


@dataclass
class SectionSpec:
    """Specification for a manuscript section."""

    id: str  # "intro", "background", "method", etc.
    title: str
    order: int

    purpose: str  # Purpose of this section
    key_points: List[str]  # Key points to cover

    target_length: int  # words
    subsections: List[str] = field(default_factory=list)

    relevant_findings: List[str] = field(default_factory=list)  # Finding IDs
    relevant_references: List[int] = field(default_factory=list)  # Reference IDs

    dependencies: List[str] = field(default_factory=list)  # Section IDs needed first

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "order": self.order,
            "purpose": self.purpose,
            "key_points": self.key_points,
            "target_length": self.target_length,
            "subsections": self.subsections,
            "relevant_findings": self.relevant_findings,
            "relevant_references": self.relevant_references,
            "dependencies": self.dependencies
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SectionSpec":
        return cls(
            id=data["id"],
            title=data["title"],
            order=data["order"],
            purpose=data["purpose"],
            key_points=data["key_points"],
            target_length=data["target_length"],
            subsections=data.get("subsections", []),
            relevant_findings=data.get("relevant_findings", []),
            relevant_references=data.get("relevant_references", []),
            dependencies=data.get("dependencies", [])
        )


@dataclass
class ManuscriptPlan:
    """Complete manuscript structure plan."""

    title: str
    abstract_outline: str

    sections: List[SectionSpec] = field(default_factory=list)

    target_length: int = 4000  # Total words
    citation_style: str = "numbered"  # "numbered", "author-year"

    overall_narrative: str = ""  # Story arc

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "abstract_outline": self.abstract_outline,
            "sections": [s.to_dict() for s in self.sections],
            "target_length": self.target_length,
            "citation_style": self.citation_style,
            "overall_narrative": self.overall_narrative
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ManuscriptPlan":
        return cls(
            title=data["title"],
            abstract_outline=data["abstract_outline"],
            sections=[SectionSpec.from_dict(s) for s in data.get("sections", [])],
            target_length=data.get("target_length", 4000),
            citation_style=data.get("citation_style", "numbered"),
            overall_narrative=data.get("overall_narrative", "")
        )


@dataclass
class Subsection:
    """Subsection within a section."""

    title: str
    content: str
    word_count: int


@dataclass
class SectionDraft:
    """Written section draft."""

    id: str
    title: str
    content: str  # Markdown

    word_count: int
    citations: List[int] = field(default_factory=list)  # Used reference IDs

    subsections: List[Subsection] = field(default_factory=list)

    author: str = ""  # Lead or coauthor name
    status: Literal["draft", "reviewed", "finalized"] = "draft"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "word_count": self.word_count,
            "citations": self.citations,
            "subsections": [
                {"title": s.title, "content": s.content, "word_count": s.word_count}
                for s in self.subsections
            ],
            "author": self.author,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SectionDraft":
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            word_count=data["word_count"],
            citations=data.get("citations", []),
            subsections=[
                Subsection(s["title"], s["content"], s["word_count"])
                for s in data.get("subsections", [])
            ],
            author=data.get("author", ""),
            status=data.get("status", "draft")
        )


@dataclass
class SectionFeedback:
    """Feedback on a section from co-author."""

    section_id: str
    reviewer: str  # Coauthor name

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    clarity_score: int = 3  # 1-5
    technical_accuracy: int = 3  # 1-5
    completeness: int = 3  # 1-5

    def to_dict(self) -> dict:
        return {
            "section_id": self.section_id,
            "reviewer": self.reviewer,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "suggestions": self.suggestions,
            "clarity_score": self.clarity_score,
            "technical_accuracy": self.technical_accuracy,
            "completeness": self.completeness
        }


@dataclass
class Manuscript:
    """Complete manuscript."""

    title: str
    abstract: str
    content: str  # Full markdown
    references: str  # References section

    word_count: int
    citation_count: int

    sections: List[SectionDraft] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "abstract": self.abstract,
            "content": self.content,
            "references": self.references,
            "word_count": self.word_count,
            "citation_count": self.citation_count,
            "sections": [s.to_dict() for s in self.sections]
        }
