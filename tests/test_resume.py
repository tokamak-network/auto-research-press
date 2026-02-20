#!/usr/bin/env python3
"""Test script to resume workflow from checkpoint."""

import asyncio
import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("GOOGLE_API_KEY"),
    reason="API keys not set",
)

from research_cli.workflow.orchestrator import WorkflowOrchestrator


def test_resume():
    asyncio.get_event_loop().run_until_complete(_test_resume())


async def _test_resume():
    """Resume workflow from checkpoint."""
    output_dir = Path("results/quantum-computing-in-drug-discovery")

    print(f"Attempting to resume from: {output_dir}")

    try:
        result = await WorkflowOrchestrator.resume_from_checkpoint(output_dir)
        print("\n✓ Workflow resumed and completed successfully!")
        print(f"Final status: {result.get('status')}")
        print(f"Total rounds: {result.get('total_rounds')}")

        return result
    except Exception as e:
        print(f"\n✗ Resume failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_resume())
