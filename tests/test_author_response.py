#!/usr/bin/env python3
"""Test author response workflow."""

import asyncio
import json
from pathlib import Path
from research_cli.agents.writer import WriterAgent


async def test_author_response_generation():
    """Test author response generation on historical review data."""

    # Load historical review data
    data_file = Path("web/data/based-rollup-20260205-234749.json")
    with open(data_file) as f:
        data = json.load(f)

    print("=" * 80)
    print("TESTING AUTHOR RESPONSE GENERATION")
    print("=" * 80)
    print(f"\nProject: {data['topic']}")
    print(f"Using Round 1 reviews to generate author response\n")

    # Get Round 1 data
    round_1 = data['rounds'][0]
    reviews = round_1['reviews']

    print(f"Round 1 Average Score: {round_1['overall_average']}/10")
    print(f"Number of reviewers: {len(reviews)}\n")

    print("Reviewer scores:")
    for review in reviews:
        print(f"  - {review['specialist_name']}: {review['average']}/10")

    # Generate author response
    print(f"\n{'=' * 80}")
    print("GENERATING AUTHOR RESPONSE...")
    print(f"{'=' * 80}\n")

    writer = WriterAgent()

    # Note: We don't have the actual manuscript, so we'll use a placeholder
    manuscript = "[Manuscript content - Based Rollup analysis]"

    author_response = await writer.write_author_response(
        manuscript=manuscript,
        reviews=reviews,
        round_number=1
    )

    print("AUTHOR RESPONSE:")
    print("=" * 80)
    print(author_response)
    print("=" * 80)

    # Analyze response structure
    print("\n\nRESPONSE ANALYSIS:")
    print(f"  Length: {len(author_response)} characters")
    print(f"  Word count: {len(author_response.split())} words")

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
        if section.lower() in author_response.lower():
            print(f"    ✓ {section}")
        else:
            print(f"    ✗ {section}")

    print("\n  Addresses all reviewers:")
    for i, review in enumerate(reviews, 1):
        reviewer_name = review['specialist_name']
        if reviewer_name in author_response or f"Reviewer {i}" in author_response:
            print(f"    ✓ {reviewer_name}")
        else:
            print(f"    ✗ {reviewer_name}")


if __name__ == "__main__":
    asyncio.run(test_author_response_generation())
