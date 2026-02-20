"""Tests for topic category classification fixes.

Proves:
1. Keyword fallback correctly classifies biology/medicine topics (no more CS default)
2. suggest_category_llm falls back gracefully when LLM fails
3. Default for unknown topics is no longer computer_science/theory
4. Desk editor receives and uses category information
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import dataclass

import pytest

from research_cli.categories import (
    suggest_category_from_topic,
    suggest_category_llm,
    ACADEMIC_CATEGORIES,
)


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


# ---------------------------------------------------------------------------
# Keyword fallback: biology/medicine topics must NOT fall to CS
# ---------------------------------------------------------------------------

class TestKeywordFallback:
    """suggest_category_from_topic should classify bio/med topics correctly."""

    def test_crispr_classified_as_biology(self):
        result = suggest_category_from_topic("CRISPR gene editing")
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_gene_therapy_classified_as_biology(self):
        result = suggest_category_from_topic("gene therapy for sickle cell")
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_genome_classified_as_biology(self):
        result = suggest_category_from_topic("whole genome sequencing")
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_stem_cell_classified_as_biology(self):
        result = suggest_category_from_topic("stem cell differentiation")
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_cancer_treatment_classified_as_medicine(self):
        result = suggest_category_from_topic("cancer treatment immunotherapy")
        assert result["major"] == "medicine_health"
        assert result["subfield"] == "clinical"

    def test_immune_therapy_classified_as_medicine(self):
        result = suggest_category_from_topic("immune checkpoint inhibitors")
        assert result["major"] == "medicine_health"
        assert result["subfield"] == "clinical"

    def test_enzyme_classified_as_biology(self):
        result = suggest_category_from_topic("enzyme engineering")
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_virus_classified_as_biology(self):
        result = suggest_category_from_topic("virus mutation patterns")
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_unknown_topic_returns_none_major(self):
        """Completely unknown topic should return major=None, not CS."""
        # Use a string that doesn't substring-match any keyword
        # (e.g. "ux" matches inside "quux", so avoid that)
        result = suggest_category_from_topic("zzznonsensewordzzz")
        assert result["major"] is None
        assert result["subfield"] is None

    def test_existing_cs_topics_still_work(self):
        """Existing CS keyword matching should not break."""
        result = suggest_category_from_topic("deep learning for NLP")
        assert result["major"] == "computer_science"
        assert result["subfield"] == "ai_ml"

    def test_existing_physics_still_works(self):
        result = suggest_category_from_topic("quantum entanglement")
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "physics"

    def test_blockchain_still_cs_security(self):
        result = suggest_category_from_topic("blockchain consensus mechanisms")
        assert result["major"] == "computer_science"
        assert result["subfield"] == "security"


# ---------------------------------------------------------------------------
# LLM classifier: graceful fallback when LLM fails
# ---------------------------------------------------------------------------

class TestSuggestCategoryLlm:
    def test_llm_success_returns_llm_result(self):
        """When LLM returns valid category, use it."""
        @dataclass
        class FakeResponse:
            content: str = "natural_sciences/biology"
            total_tokens: int = 10
            input_tokens: int = 5
            output_tokens: int = 5

        fake_llm = MagicMock()
        fake_llm.generate = AsyncMock(return_value=FakeResponse())

        with patch("research_cli.model_config.create_llm_for_role", return_value=fake_llm):
            result = _run(suggest_category_llm("CRISPR gene editing"))

        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_llm_failure_falls_back_to_keywords(self):
        """When LLM raises exception, fall back to keyword matching."""
        with patch("research_cli.model_config.create_llm_for_role", side_effect=Exception("no API key")):
            result = _run(suggest_category_llm("deep learning for NLP"))

        # Keywords should match AI/ML
        assert result["major"] == "computer_science"
        assert result["subfield"] == "ai_ml"

    def test_llm_failure_with_bio_topic_uses_keyword_bio(self):
        """When LLM fails on a bio topic, keyword fallback should catch it."""
        with patch("research_cli.model_config.create_llm_for_role", side_effect=Exception("timeout")):
            result = _run(suggest_category_llm("CRISPR gene editing"))

        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"

    def test_llm_failure_unknown_topic_not_cs(self):
        """When both LLM and keywords fail, should NOT return CS/theory."""
        with patch("research_cli.model_config.create_llm_for_role", side_effect=Exception("no key")):
            result = _run(suggest_category_llm("zzznonsensewordzzz"))

        # Should fall back to natural_sciences/biology (safe default), not CS/theory
        assert result["major"] != "computer_science"
        assert result["major"] is not None

    def test_llm_returns_garbage_falls_back(self):
        """When LLM returns unparseable text, fall back to keywords."""
        @dataclass
        class FakeResponse:
            content: str = "I think this is about something or other"
            total_tokens: int = 10
            input_tokens: int = 5
            output_tokens: int = 5

        fake_llm = MagicMock()
        fake_llm.generate = AsyncMock(return_value=FakeResponse())

        with patch("research_cli.model_config.create_llm_for_role", return_value=fake_llm):
            result = _run(suggest_category_llm("CRISPR gene editing"))

        # Should fall back to keyword matching → biology
        assert result["major"] == "natural_sciences"
        assert result["subfield"] == "biology"


# ---------------------------------------------------------------------------
# Desk editor: category parameter
# ---------------------------------------------------------------------------

class TestDeskEditorCategory:
    def test_screen_accepts_category_parameter(self):
        """DeskEditorAgent.screen() should accept optional category param."""
        from research_cli.agents.desk_editor import DeskEditorAgent

        # Verify the method signature accepts category
        import inspect
        sig = inspect.signature(DeskEditorAgent.screen)
        params = list(sig.parameters.keys())
        assert "category" in params

    def test_screen_category_included_in_prompt(self):
        """When category is provided, it should appear in the prompt sent to LLM."""
        from research_cli.agents.desk_editor import DeskEditorAgent

        @dataclass
        class FakeResponse:
            content: str = '{"decision": "PASS", "reason": "looks good"}'
            total_tokens: int = 10
            input_tokens: int = 5
            output_tokens: int = 5

        fake_llm = MagicMock()
        fake_llm.generate = AsyncMock(return_value=FakeResponse())
        fake_llm.model = "test-model"

        with patch("research_cli.agents.desk_editor.create_llm_for_role", return_value=fake_llm):
            agent = DeskEditorAgent()
            result = _run(agent.screen(
                "Some manuscript about CRISPR...",
                "CRISPR gene editing",
                category="Computer Science (Theory & Algorithms)"
            ))

        # Check that generate was called with a prompt containing the category
        call_kwargs = fake_llm.generate.call_args
        prompt_sent = call_kwargs.kwargs.get("prompt", "")

        assert "Computer Science (Theory & Algorithms)" in prompt_sent
        assert "academic field" in prompt_sent

    def test_screen_without_category_still_works(self):
        """screen() without category should work as before (backward compatible)."""
        from research_cli.agents.desk_editor import DeskEditorAgent

        @dataclass
        class FakeResponse:
            content: str = '{"decision": "PASS", "reason": "ok"}'
            total_tokens: int = 10
            input_tokens: int = 5
            output_tokens: int = 5

        fake_llm = MagicMock()
        fake_llm.generate = AsyncMock(return_value=FakeResponse())
        fake_llm.model = "test-model"

        with patch("research_cli.agents.desk_editor.create_llm_for_role", return_value=fake_llm):
            agent = DeskEditorAgent()
            result = _run(agent.screen("Some manuscript...", "some topic"))

        assert result["decision"] == "PASS"

    def test_screen_without_category_no_field_check(self):
        """Without category, prompt should NOT contain field mismatch check."""
        from research_cli.agents.desk_editor import DeskEditorAgent

        @dataclass
        class FakeResponse:
            content: str = '{"decision": "PASS", "reason": "ok"}'
            total_tokens: int = 10
            input_tokens: int = 5
            output_tokens: int = 5

        fake_llm = MagicMock()
        fake_llm.generate = AsyncMock(return_value=FakeResponse())
        fake_llm.model = "test-model"

        with patch("research_cli.agents.desk_editor.create_llm_for_role", return_value=fake_llm):
            agent = DeskEditorAgent()
            _run(agent.screen("Some manuscript...", "some topic"))

        prompt_sent = fake_llm.generate.call_args.kwargs.get("prompt", "")
        assert "academic field" not in prompt_sent
        assert "Assigned academic field" not in prompt_sent


# ---------------------------------------------------------------------------
# Integration: CLI import paths
# ---------------------------------------------------------------------------

class TestCliImportPaths:
    def test_cli_uses_llm_classifier_not_keyword(self):
        """Verify cli.py imports suggest_category_llm, not suggest_category_from_topic."""
        import importlib
        import inspect

        source = inspect.getsource(importlib.import_module("research_cli.cli"))

        # The collaborative run function should use suggest_category_llm
        assert "suggest_category_llm" in source
        # The actual category assignment should use the LLM version
        assert "await suggest_category_llm(topic)" in source
