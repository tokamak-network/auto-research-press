"""System integrity tests — no LLM calls, zero cost, runs in seconds.

Validates that code changes haven't broken imports, configs, data models,
API endpoints, static assets, or the citation pipeline.

Usage:
    python3 -m pytest tests/test_integrity.py -v
"""

import json
import importlib
from pathlib import Path

import pytest

# Project root
ROOT = Path(__file__).resolve().parent.parent


# ── 1-1. Import & Module Integrity ──────────────────────────────────────────

class TestImports:
    """Every core module must import without error."""

    @pytest.mark.parametrize("module", [
        "research_cli.agents.lead_author",
        "research_cli.agents.coauthor",
        "research_cli.agents.team_composer",
        "research_cli.agents.writer_team_composer",
        "research_cli.agents.moderator",
        "research_cli.agents.specialist_factory",
        "research_cli.agents.writer",
        "research_cli.agents.integration_editor",
        "research_cli.workflow.collaborative_research",
        "research_cli.workflow.manuscript_writing",
        "research_cli.workflow.collaborative_workflow",
        "research_cli.workflow.orchestrator",
        "research_cli.utils.source_retriever",
        "research_cli.utils.citation_manager",
        "research_cli.utils.json_repair",
        "research_cli.model_config",
        "research_cli.categories",
        "research_cli.performance",
        "research_cli.models.manuscript",
        "research_cli.models.collaborative_research",
        "research_cli.models.author",
        "research_cli.models.expert",
    ])
    def test_import_module(self, module):
        importlib.import_module(module)

    def test_import_export_to_web(self):
        importlib.import_module("export_to_web")


# ── 1-2. Config Integrity ──────────────────────────────────────────────────

class TestConfig:
    """config/models.json must parse correctly with required structure."""

    @pytest.fixture(scope="class")
    def config(self):
        path = ROOT / "config" / "models.json"
        assert path.exists(), "config/models.json not found"
        with open(path) as f:
            return json.load(f)

    def test_config_parses(self, config):
        assert isinstance(config, dict)

    def test_required_roles_exist(self, config):
        roles = config.get("roles", {})
        for required in ("lead_author", "coauthor", "reviewer_rotation"):
            assert required in roles, f"Missing required role: {required}"

    def test_reviewer_rotation_has_3_plus(self, config):
        rotation = config["roles"]["reviewer_rotation"]
        assert isinstance(rotation, list)
        assert len(rotation) >= 3, f"reviewer_rotation has only {len(rotation)} entries (need >=3)"

    def test_role_provider_model_pairs(self, config):
        roles = config.get("roles", {})
        tiers = config.get("tiers", {})
        for role_name, role_cfg in roles.items():
            if role_name == "reviewer_rotation":
                for entry in role_cfg:
                    assert "provider" in entry, f"reviewer_rotation entry missing 'provider'"
                    assert "model" in entry, f"reviewer_rotation entry missing 'model'"
                continue
            if isinstance(role_cfg, dict) and "tier" in role_cfg:
                tier_name = role_cfg["tier"]
                assert tier_name in tiers, f"Role '{role_name}' references unknown tier '{tier_name}'"

    def test_tiers_have_primary(self, config):
        tiers = config.get("tiers", {})
        for tier_name, tier in tiers.items():
            assert "primary" in tier, f"Tier '{tier_name}' missing 'primary'"
            primary = tier["primary"]
            assert "model" in primary, f"Tier '{tier_name}' primary missing 'model'"
            assert "provider" in primary, f"Tier '{tier_name}' primary missing 'provider'"

    def test_pricing_section_exists(self, config):
        assert "pricing" in config, "Missing 'pricing' section"
        pricing = config["pricing"]
        assert len(pricing) > 0, "Pricing section is empty"
        for model_name, prices in pricing.items():
            assert "input" in prices, f"Pricing for '{model_name}' missing 'input'"
            assert "output" in prices, f"Pricing for '{model_name}' missing 'output'"


# ── 1-3. API Endpoint Integrity ─────────────────────────────────────────────

class TestAPIEndpoints:
    """api_server.py must import and expose required endpoints."""

    @pytest.fixture(scope="class")
    def app(self):
        pytest.importorskip("fastapi")
        from api_server import app
        return app

    def test_app_import(self, app):
        assert app is not None

    @pytest.mark.parametrize("path,method", [
        ("/api/health", "GET"),
        ("/api/start-workflow", "POST"),
        ("/api/workflows", "GET"),
        ("/api/workflow-status/{project_id}", "GET"),
        ("/api/classify-topic", "POST"),
        ("/api/propose-team", "POST"),
        ("/api/version", "GET"),
    ])
    def test_endpoint_exists(self, app, path, method):
        """Check that required endpoint exists with correct HTTP method."""
        route_paths = {}
        for route in app.routes:
            if hasattr(route, "path") and hasattr(route, "methods"):
                route_paths[route.path] = route.methods

        assert path in route_paths, f"Endpoint {path} not found in app routes"
        assert method in route_paths[path], (
            f"Endpoint {path} exists but method {method} not found "
            f"(has: {route_paths[path]})"
        )


# ── 1-4. Web Static File Integrity ──────────────────────────────────────────

class TestWebStaticFiles:
    """Required HTML, CSS, JS files must exist."""

    @pytest.mark.parametrize("filename", [
        "index.html",
        "article.html",
        "ask-topic.html",
        "submit.html",
        "review.html",
    ])
    def test_html_page_exists(self, filename):
        path = ROOT / "web" / filename
        assert path.exists(), f"Missing web page: web/{filename}"

    def test_main_css_exists(self):
        assert (ROOT / "web" / "styles" / "main.css").exists()

    def test_js_directory_exists(self):
        assert (ROOT / "web" / "js").is_dir()


# ── 1-5. Citation Pipeline Unit Tests ───────────────────────────────────────

class TestCitationPipeline:
    """CitationManager must correctly extract, validate, and count citations."""

    @pytest.fixture(scope="class")
    def cm(self):
        from research_cli.utils.citation_manager import CitationManager
        return CitationManager

    @pytest.fixture(scope="class")
    def make_ref(self):
        from research_cli.models.collaborative_research import Reference
        def _make(ref_id):
            return Reference(
                id=ref_id, authors=["Author"], title=f"Paper {ref_id}",
                venue="Journal", year=2025
            )
        return _make

    def test_extract_simple(self, cm):
        assert cm.extract_citations("[1], [2] and [3]") == [1, 2, 3]

    def test_extract_grouped(self, cm):
        assert cm.extract_citations("[1,2,3]") == [1, 2, 3]

    def test_extract_mixed(self, cm):
        result = cm.extract_citations("[1], [2,3] and [4]")
        assert result == [1, 2, 3, 4]

    def test_extract_empty(self, cm):
        assert cm.extract_citations("No citations here.") == []

    def test_extract_deduplicates(self, cm):
        result = cm.extract_citations("[1] and [1,2]")
        assert result == [1, 2]

    def test_validate_all_matched(self, cm, make_ref):
        refs = [make_ref(1), make_ref(2), make_ref(3)]
        text = "As shown in [1] and [2,3]."
        is_valid, errors = cm.validate_citations(text, refs)
        assert is_valid
        assert errors == []

    def test_validate_missing_reference(self, cm, make_ref):
        refs = [make_ref(1)]
        text = "As shown in [1] and [5]."
        is_valid, errors = cm.validate_citations(text, refs)
        assert not is_valid
        assert len(errors) == 1
        assert "[5]" in errors[0]

    def test_statistics_accuracy(self, cm, make_ref):
        refs = [make_ref(1), make_ref(2), make_ref(3), make_ref(4)]
        text = "See [1] and [2,3]."
        stats = cm.get_citation_statistics(text, refs)
        assert stats["total_citations"] == 3
        assert stats["unique_citations"] == 3
        assert stats["total_references"] == 4
        assert stats["unused_references"] == 1
        assert 4 in stats["unused_reference_ids"]

    def test_format_inline_citation(self, cm):
        assert cm.format_inline_citation([1, 2, 3]) == "[1,2,3]"


# ── 1-6. Model / Data Structure Integrity ────────────────────────────────────

class TestDataModels:
    """Data model serialization round-trips must be identity."""

    def test_section_spec_relevant_references_field(self):
        from research_cli.models.manuscript import SectionSpec
        spec = SectionSpec(
            id="intro", title="Introduction", order=1,
            purpose="Introduce the topic", key_points=["point1"],
            target_length=500
        )
        assert hasattr(spec, "relevant_references")
        assert spec.relevant_references == []

    def test_section_spec_roundtrip(self):
        from research_cli.models.manuscript import SectionSpec
        original = SectionSpec(
            id="bg", title="Background", order=2,
            purpose="Background info", key_points=["a", "b"],
            target_length=800,
            relevant_references=[1, 3, 5],
            relevant_findings=["f1"],
        )
        restored = SectionSpec.from_dict(original.to_dict())
        assert restored.to_dict() == original.to_dict()

    def test_manuscript_plan_roundtrip(self):
        from research_cli.models.manuscript import ManuscriptPlan, SectionSpec
        plan = ManuscriptPlan(
            title="Test Plan",
            abstract_outline="An outline",
            sections=[
                SectionSpec(
                    id="intro", title="Intro", order=1,
                    purpose="Purpose", key_points=["kp"],
                    target_length=300, relevant_references=[1]
                ),
            ],
            target_length=2000,
        )
        restored = ManuscriptPlan.from_dict(plan.to_dict())
        assert restored.to_dict() == plan.to_dict()

    def test_section_draft_roundtrip(self):
        from research_cli.models.manuscript import SectionDraft
        draft = SectionDraft(
            id="intro", title="Intro", content="Hello world",
            word_count=2, citations=[1, 2], author="Lead"
        )
        restored = SectionDraft.from_dict(draft.to_dict())
        assert restored.to_dict() == draft.to_dict()

    def test_manuscript_to_dict(self):
        from research_cli.models.manuscript import Manuscript
        ms = Manuscript(
            title="Title", abstract="Abstract", content="Body",
            references="Refs", word_count=100, citation_count=5
        )
        d = ms.to_dict()
        assert d["title"] == "Title"
        assert d["word_count"] == 100

    def test_reference_roundtrip(self):
        from research_cli.models.collaborative_research import Reference
        ref = Reference(
            id=1, authors=["Alice", "Bob"], title="Paper",
            venue="ICML", year=2024, url="https://example.com",
            doi="10.1234/test", summary="Good paper"
        )
        restored = Reference.from_dict(ref.to_dict())
        assert restored.to_dict() == ref.to_dict()

    def test_finding_roundtrip(self):
        from research_cli.models.collaborative_research import Finding
        finding = Finding(
            id="f1", title="Finding 1", description="Desc",
            evidence="Evidence text", citations=[1, 2],
            author="Lead", confidence="high", timestamp="2025-01-01T00:00:00"
        )
        restored = Finding.from_dict(finding.to_dict())
        assert restored.to_dict() == finding.to_dict()

    def test_collaborative_research_notes_roundtrip(self):
        from research_cli.models.collaborative_research import (
            CollaborativeResearchNotes, Reference, Finding
        )
        notes = CollaborativeResearchNotes(
            research_questions=["RQ1"],
            hypotheses=["H1"],
            references=[
                Reference(id=1, authors=["A"], title="T", venue="V", year=2024)
            ],
            findings=[
                Finding(
                    id="f1", title="F", description="D", evidence="E",
                    citations=[1], author="lead", confidence="high",
                    timestamp="2025-01-01T00:00:00"
                )
            ],
            version=1,
        )
        d = notes.to_dict()
        restored = CollaborativeResearchNotes.from_dict(d)
        # Check core fields survived the round-trip
        assert len(restored.references) == 1
        assert restored.references[0].to_dict() == notes.references[0].to_dict()
        assert len(restored.findings) == 1
        assert restored.findings[0].to_dict() == notes.findings[0].to_dict()
        assert restored.research_questions == ["RQ1"]

    def test_author_role_roundtrip(self):
        from research_cli.models.author import AuthorRole
        author = AuthorRole(
            id="lead-1", name="Dr. Smith", role="lead",
            expertise="AI", focus_areas=["NLP", "CV"],
        )
        restored = AuthorRole.from_dict(author.to_dict())
        assert restored.to_dict() == author.to_dict()

    def test_writer_team_roundtrip(self):
        from research_cli.models.author import AuthorRole, WriterTeam
        team = WriterTeam(
            lead_author=AuthorRole(
                id="lead", name="Lead", role="lead",
                expertise="ML", focus_areas=["deep learning"]
            ),
            coauthors=[
                AuthorRole(
                    id="co1", name="Co1", role="coauthor",
                    expertise="NLP", focus_areas=["transformers"]
                )
            ]
        )
        restored = WriterTeam.from_dict(team.to_dict())
        assert restored.to_dict() == team.to_dict()


# ── 1-7. CLI Command Integrity ───────────────────────────────────────────────

class TestCLI:
    """CLI must parse arguments and show help without errors."""

    def test_cli_help(self):
        from click.testing import CliRunner
        from research_cli.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "research workflow" in result.output.lower() or "Usage" in result.output

    def test_run_help(self):
        from click.testing import CliRunner
        from research_cli.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0

    @pytest.mark.parametrize("option,values", [
        ("--article-length", ["short", "full"]),
        ("--audience-level", ["beginner", "intermediate", "professional"]),
        ("--research-type", ["explainer", "survey", "original"]),
    ])
    def test_run_option_in_help(self, option, values):
        from click.testing import CliRunner
        from research_cli.cli import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert option in result.output, f"Option '{option}' not found in run --help"
        for val in values:
            assert val in result.output, f"Value '{val}' not found in run --help for {option}"


# ── 1-8. Export Pipeline Integrity ───────────────────────────────────────────

class TestExportPipeline:
    """export_to_web.generate_article_html must be callable with sample data."""

    def test_generate_article_html_callable(self):
        from export_to_web import generate_article_html
        import inspect
        sig = inspect.signature(generate_article_html)
        params = list(sig.parameters.keys())
        assert "project_id" in params
        assert "workflow_data" in params
        assert "manuscript_text" in params

    def test_generate_article_html_with_sample_data(self):
        from export_to_web import generate_article_html
        workflow_data = {
            "topic": "Test Topic",
            "rounds": [
                {
                    "overall_average": 7.5,
                    "moderator_decision": {"decision": "ACCEPT"},
                }
            ],
            "expert_team": [
                {"name": "Expert 1"},
                {"name": "Expert 2"},
            ],
        }
        manuscript_text = (
            "# Test Article\n\n"
            "## Introduction\n\n"
            "This is a test article with citation [1].\n\n"
            "## Conclusion\n\n"
            "We conclude with [2].\n\n"
            "## References\n\n"
            "[1] Author (2024). Title. Venue.\n"
            "[2] Author (2024). Title2. Venue2.\n"
        )
        html = generate_article_html("test-project", workflow_data, manuscript_text)
        assert isinstance(html, str)
        assert len(html) > 100
        assert "Test Article" in html or "test-project" in html
