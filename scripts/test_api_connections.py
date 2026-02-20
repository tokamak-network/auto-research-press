#!/usr/bin/env python3
"""Test API connections for all configured models.

Usage:
    python scripts/test_api_connections.py
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from research_cli.model_config import (
    _load_config, _create_llm, get_role_config, get_reviewer_models,
)


async def test_model(provider: str, model: str) -> dict:
    """Test a single model with a minimal prompt."""
    try:
        llm = _create_llm(provider, model)
        response = await llm.generate(
            prompt="Say hello in exactly 5 words.",
            temperature=0.1,
            max_tokens=50,
        )
        return {
            "model": model,
            "provider": provider,
            "status": "OK",
            "response": response.content[:80],
            "tokens": f"in={response.input_tokens} out={response.output_tokens}",
        }
    except Exception as e:
        return {
            "model": model,
            "provider": provider,
            "status": "FAIL",
            "error": str(e)[:120],
        }


async def main():
    config = _load_config()

    # Collect unique model+provider pairs from tiers + reviewer_rotation
    seen = set()
    tests = []

    # From tiers
    for tier_name, tier_data in config.get("tiers", {}).items():
        primary = tier_data["primary"]
        key = (primary["provider"], primary["model"])
        if key not in seen:
            seen.add(key)
            tests.append(key)
        for fb in tier_data.get("fallback", []):
            key = (fb["provider"], fb["model"])
            if key not in seen:
                seen.add(key)
                tests.append(key)

    # From reviewer_rotation
    for r in config.get("roles", {}).get("reviewer_rotation", []):
        key = (r["provider"], r["model"])
        if key not in seen:
            seen.add(key)
            tests.append(key)
        for fb in r.get("fallback", []):
            key = (fb["provider"], fb["model"])
            if key not in seen:
                seen.add(key)
                tests.append(key)

    print(f"Testing {len(tests)} unique model+provider combinations...\n")
    print(f"{'Provider':12s} {'Model':30s} {'Status':8s} {'Details'}")
    print("-" * 100)

    results = await asyncio.gather(*[test_model(p, m) for p, m in tests])

    ok = 0
    fail = 0
    for r in results:
        if r["status"] == "OK":
            detail = f"{r['response'][:50]}  ({r['tokens']})"
            ok += 1
        else:
            detail = r["error"]
            fail += 1
        print(f"{r['provider']:12s} {r['model']:30s} {r['status']:8s} {detail}")

    print(f"\n{'='*100}")
    print(f"Result: {ok} OK, {fail} FAIL out of {len(tests)} models")
    return fail == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
