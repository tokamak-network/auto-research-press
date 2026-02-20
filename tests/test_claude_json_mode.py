"""Minimal test: Claude API handles json_mode parameter without error.

Uses claude-haiku-4-5 (cheapest) with a tiny prompt to verify:
1. json_mode=True is silently ignored (no crash)
2. Response still contains valid JSON when prompted for it
"""

import asyncio
import json
import os
import pytest

from research_cli.llm.claude import ClaudeLLM


@pytest.fixture
def claude_llm():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    return ClaudeLLM(api_key=api_key, model="claude-haiku-4-5")


def test_claude_json_mode_no_crash(claude_llm):
    """json_mode=True must not raise — Claude silently ignores it."""
    response = asyncio.get_event_loop().run_until_complete(claude_llm.generate(
        prompt='Return JSON: {"status": "ok"}',
        system="Respond with only valid JSON, no markdown.",
        temperature=0.0,
        max_tokens=32,
        json_mode=True,
    ))
    assert response.content.strip()
    # Claude doesn't have native json_mode, so it may wrap in ```json.
    # In production repair_json handles this. Here just verify no crash
    # and that the JSON content is present somewhere in the response.
    from research_cli.utils.json_repair import repair_json
    data = repair_json(response.content)
    assert "status" in data
