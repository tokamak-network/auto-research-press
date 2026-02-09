"""Integration tests for the full team pipeline: category → reviewers → co-authors.

Uses real LLM calls to verify end-to-end behavior across diverse topics.
Run with: python3 -m pytest tests/test_team_pipeline.py -v -m llm
"""

import sys
from unittest.mock import MagicMock

# Stub out heavy server dependencies so api_server can be imported without
# fastapi/uvicorn/gunicorn being installed. MagicMock handles arbitrary
# attribute access and calls, which is needed for module-level side effects
# like `app = FastAPI(...)`, `app.add_middleware(...)`, and `@app.get(...)`.
_stub_modules = [
    "fastapi", "fastapi.middleware", "fastapi.middleware.cors",
    "fastapi.responses", "fastapi.staticfiles",
    "uvicorn", "gunicorn",
]
for mod_name in _stub_modules:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MagicMock()

import pytest
from research_cli.categories import suggest_category_llm, ACADEMIC_CATEGORIES
from research_cli.agents.team_composer import TeamComposerAgent

# Now safe to import api_server
import importlib
api_server = importlib.import_module("api_server")
_generate_reviewers_from_category = api_server._generate_reviewers_from_category

pytestmark = pytest.mark.llm

# Diverse test topics spanning multiple academic fields
TOPICS = [
    "Transformer 아키텍처의 Attention 메커니즘 최적화",
    "기후변화가 해양 생태계에 미치는 영향",
    "CRISPR-Cas9 유전자 편집의 윤리적 문제",
    "블록체인 기반 탈중앙화 금융(DeFi)의 리스크 분석",
    "양자컴퓨팅이 현대 암호학에 미치는 위협",
]


def _valid_major_subfield(major: str, subfield: str) -> bool:
    """Check that major/subfield exist in ACADEMIC_CATEGORIES."""
    return (
        major in ACADEMIC_CATEGORIES
        and subfield in ACADEMIC_CATEGORIES[major]["subfields"]
    )


class TestCategoryDetection:
    """LLM-based category detection for diverse topics."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("topic", TOPICS, ids=[
        "transformer_attention",
        "climate_ocean",
        "crispr_ethics",
        "defi_risk",
        "quantum_crypto",
    ])
    async def test_category_returns_valid_major_subfield(self, topic: str):
        result = await suggest_category_llm(topic)
        assert "major" in result, f"Missing 'major' key for topic: {topic}"
        assert "subfield" in result, f"Missing 'subfield' key for topic: {topic}"
        assert _valid_major_subfield(result["major"], result["subfield"]), (
            f"Invalid category {result['major']}/{result['subfield']} for topic: {topic}"
        )


class TestReviewerGeneration:
    """LLM-based reviewer generation for diverse topics."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("topic", TOPICS, ids=[
        "transformer_attention",
        "climate_ocean",
        "crispr_ethics",
        "defi_risk",
        "quantum_crypto",
    ])
    async def test_generates_3_unique_reviewers(self, topic: str):
        category = await suggest_category_llm(topic)
        reviewers = await _generate_reviewers_from_category(category, topic)

        assert len(reviewers) == 3, f"Expected 3 reviewers, got {len(reviewers)}"

        for i, rev in enumerate(reviewers):
            assert rev.name, f"Reviewer {i+1} missing name"
            assert rev.domain, f"Reviewer {i+1} missing domain"
            assert isinstance(rev.focus_areas, list), f"Reviewer {i+1} focus_areas not a list"
            assert len(rev.focus_areas) > 0, f"Reviewer {i+1} has no focus_areas"

        # Check no duplicate domains
        domains = [r.domain for r in reviewers]
        assert len(set(domains)) == len(domains), f"Duplicate reviewer domains: {domains}"


class TestTeamComposition:
    """LLM-based co-author team proposal for diverse topics."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("topic", TOPICS, ids=[
        "transformer_attention",
        "climate_ocean",
        "crispr_ethics",
        "defi_risk",
        "quantum_crypto",
    ])
    async def test_proposes_3_coauthors(self, topic: str):
        composer = TeamComposerAgent()
        proposals = await composer.propose_team(topic, num_experts=3)

        assert len(proposals) >= 3, f"Expected >=3 proposals, got {len(proposals)}"

        for i, prop in enumerate(proposals[:3]):
            assert prop.expert_domain, f"Co-author {i+1} missing expert_domain"
            assert prop.rationale, f"Co-author {i+1} missing rationale"
            assert isinstance(prop.focus_areas, list), f"Co-author {i+1} focus_areas not a list"
            assert len(prop.focus_areas) > 0, f"Co-author {i+1} has no focus_areas"
