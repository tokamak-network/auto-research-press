#!/usr/bin/env python3
"""Test author rebuttal workflow."""

import asyncio
import json
from pathlib import Path
from research_cli.agents.writer import WriterAgent


async def test_rebuttal_generation():
    """Test rebuttal generation on historical review data."""

    # Load historical review data
    data_file = Path("web/data/based-rollup-20260205-234749.json")
    with open(data_file) as f:
        data = json.load(f)

    print("=" * 80)
    print("TESTING AUTHOR REBUTTAL GENERATION")
    print("=" * 80)
    print(f"\nProject: {data['topic']}")
    print(f"Using Round 1 reviews to generate rebuttal\n")

    # Get Round 1 data
    round_1 = data['rounds'][0]
    reviews = round_1['reviews']

    print(f"Round 1 Average Score: {round_1['overall_average']}/10")
    print(f"Number of reviewers: {len(reviews)}\n")

    print("Reviewer scores:")
    for review in reviews:
        print(f"  - {review['specialist_name']}: {review['average']}/10")

    # Generate rebuttal
    print(f"\n{'=' * 80}")
    print("GENERATING AUTHOR REBUTTAL...")
    print(f"{'=' * 80}\n")

    writer = WriterAgent()

    # Note: We don't have the actual manuscript, so we'll use a placeholder
    manuscript = "[Manuscript content - Based Rollup analysis]"

    rebuttal = await writer.write_rebuttal(
        manuscript=manuscript,
        reviews=reviews,
        round_number=1
    )

    print("AUTHOR REBUTTAL:")
    print("=" * 80)
    print(rebuttal)
    print("=" * 80)

    # Analyze rebuttal structure
    print("\n\nREBUTTAL ANALYSIS:")
    print(f"  Length: {len(rebuttal)} characters")
    print(f"  Word count: {len(rebuttal.split())} words")

    # Check for key sections
    sections = [
        "Overview",
        "Response to Reviewer",
        "Summary of Changes",
        "Action taken",
        "Our response"
    ]

    print("\n  Sections found:")
    for section in sections:
        if section.lower() in rebuttal.lower():
            print(f"    ✓ {section}")
        else:
            print(f"    ✗ {section}")

    print("\n  Addresses all reviewers:")
    for i, review in enumerate(reviews, 1):
        reviewer_name = review['specialist_name']
        if reviewer_name in rebuttal or f"Reviewer {i}" in rebuttal:
            print(f"    ✓ {reviewer_name}")
        else:
            print(f"    ✗ {reviewer_name}")


if __name__ == "__main__":
    asyncio.run(test_rebuttal_generation())
