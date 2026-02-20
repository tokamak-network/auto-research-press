#!/usr/bin/env python3
"""Test new moderator editorial judgment on existing data."""

import asyncio
import json
import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("GOOGLE_API_KEY"),
    reason="API keys not set",
)

from research_cli.agents.moderator import ModeratorAgent


def test_moderator_on_existing_data():
    asyncio.get_event_loop().run_until_complete(_test_moderator_on_existing_data())


async def _test_moderator_on_existing_data():
    """Test moderator on best performing historical project."""

    # Load best project data (Research Report - 7.9 score)
    data_file = Path("web/data/research-report.json")
    with open(data_file) as f:
        data = json.load(f)

    print("=" * 80)
    print("TESTING NEW EDITORIAL JUDGMENT ON HISTORICAL DATA")
    print("=" * 80)
    print(f"\nProject: {data['topic']}")
    print(f"Historical Final Score: {data['final_score']}")
    print(f"Historical Outcome: {'ACCEPTED' if data['passed'] else 'REJECTED'}")
    print(f"Total Rounds: {data['total_rounds']}")

    # Test Round 3 decision
    round_3 = data['rounds'][2]  # Round 3
    reviews = round_3['reviews']

    print(f"\n{'=' * 80}")
    print(f"ROUND 3 CONTEXT:")
    print(f"{'=' * 80}")
    print(f"Average Score: {round_3['overall_average']}/10")
    print(f"\nReviewer scores:")
    for review in reviews:
        print(f"  - {review['specialist_name']}: {review['average']}/10")

    print(f"\nImprovement trajectory:")
    for i, round_data in enumerate(data['rounds'], 1):
        print(f"  Round {i}: {round_data['overall_average']}/10")

    improvement = data['rounds'][2]['overall_average'] - data['rounds'][0]['overall_average']
    print(f"  Total improvement: +{improvement:.1f} points")

    # Create moderator and make decision
    print(f"\n{'=' * 80}")
    print("NEW MODERATOR DECISION WITH EDITORIAL JUDGMENT:")
    print(f"{'=' * 80}\n")

    moderator = ModeratorAgent()

    # Simulate the decision with new prompt
    decision = await moderator.make_decision(
        manuscript="[Manuscript content omitted for test]",
        reviews=reviews,
        round_number=3,
        max_rounds=3,
        previous_rounds=data['rounds'][:2]  # Pass Round 1 & 2 for trajectory
    )

    print(f"Decision: {decision['decision']}")
    print(f"Confidence: {decision['confidence']}/5")
    print(f"\nMeta-review:")
    print(decision['meta_review'])
    print(f"\nKey Strengths:")
    for strength in decision['key_strengths']:
        print(f"  • {strength}")
    print(f"\nKey Weaknesses:")
    for weakness in decision['key_weaknesses']:
        print(f"  • {weakness}")
    print(f"\nRecommendation:")
    print(decision['recommendation'])

    print(f"\n{'=' * 80}")
    print("COMPARISON:")
    print(f"{'=' * 80}")
    print(f"Old system: REJECTED (score 7.9 < threshold 8.0)")
    print(f"New system: {decision['decision']}")
    print(f"\nImprovement: {'YES ✓' if decision['decision'] == 'ACCEPT' else 'NO - needs more work'}")


if __name__ == "__main__":
    asyncio.run(test_moderator_on_existing_data())
