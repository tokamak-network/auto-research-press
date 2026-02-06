"""Author and team models for collaborative research."""

from dataclasses import dataclass, field
from typing import List, Optional, Literal


@dataclass
class AuthorRole:
    """Individual author in research team."""

    id: str
    name: str
    role: Literal["lead", "coauthor"]
    expertise: str
    focus_areas: List[str]

    # Contributions this author will make
    contributions: List[str] = field(default_factory=list)

    # LLM configuration
    provider: str = "anthropic"
    model: str = "claude-opus-4.5"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "expertise": self.expertise,
            "focus_areas": self.focus_areas,
            "contributions": self.contributions,
            "provider": self.provider,
            "model": self.model
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AuthorRole":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            role=data["role"],
            expertise=data["expertise"],
            focus_areas=data["focus_areas"],
            contributions=data.get("contributions", []),
            provider=data.get("provider", "anthropic"),
            model=data.get("model", "claude-opus-4.5")
        )


@dataclass
class WriterTeam:
    """Team of authors working on research."""

    lead_author: AuthorRole
    coauthors: List[AuthorRole] = field(default_factory=list)

    def get_all_authors(self) -> List[AuthorRole]:
        """Get all authors (lead + coauthors)."""
        return [self.lead_author] + self.coauthors

    def get_author_by_id(self, author_id: str) -> Optional[AuthorRole]:
        """Find author by ID."""
        for author in self.get_all_authors():
            if author.id == author_id:
                return author
        return None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "lead_author": self.lead_author.to_dict(),
            "coauthors": [a.to_dict() for a in self.coauthors]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WriterTeam":
        """Create from dictionary."""
        return cls(
            lead_author=AuthorRole.from_dict(data["lead_author"]),
            coauthors=[AuthorRole.from_dict(a) for a in data.get("coauthors", [])]
        )
