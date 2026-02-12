"""Moderator agent for making accept/reject decisions on peer reviews."""

from typing import List, Dict
from ..model_config import create_llm_for_role


class ModeratorAgent:
    """AI moderator that makes final accept/reject decisions.

    Acts as a journal editor-in-chief: reads reviewer scores and summaries,
    then issues a concise editorial decision with a short rationale note.
    """

    def __init__(self, role: str = "moderator"):
        """Initialize moderator agent.

        Args:
            role: Role name for model config lookup
        """
        self.llm = create_llm_for_role(role)
        self.model = self.llm.model

    async def make_decision(
        self,
        manuscript: str,
        reviews: List[Dict],
        round_number: int,
        max_rounds: int,
        previous_rounds: List[Dict] = None,
        domain: str = "interdisciplinary research",
        completeness_warning: str = None,
        outlier_info: str = None,
        threshold: float = 7.0,
    ) -> Dict:
        """Make accept/reject decision based on peer reviews.

        Returns a concise decision dict with:
        - decision: ACCEPT / MINOR_REVISION / MAJOR_REVISION / REJECT
        - confidence: 1-5
        - note: 1-3 sentence editorial rationale
        - required_changes: list (only when revision is requested)
        """
        system_prompt = f"""You are the Editor-in-Chief for a research publication in {domain}.

Make a publication decision based on peer reviews. Be decisive and concise.

Decision options:
- ACCEPT: Meets publication standards, contribution is valuable
- MINOR_REVISION: Small fixable issues, likely acceptable after revision
- MAJOR_REVISION: Substantial problems requiring significant work
- REJECT: Fundamental flaws or insufficient contribution

Threshold: {threshold}/10. Papers at or above threshold with no fatal flaws should be accepted.

STRUCTURAL COMPLETENESS (check independently of reviewer scores):
- The manuscript MUST have a concluding section (any heading containing "Conclusion",
  "Summary", "Concluding Remarks", or "Open Problems and Conclusion" counts).
- The manuscript MUST have a References/Bibliography section.
- If either is missing, issue MAJOR_REVISION (or REJECT on final round) regardless of score.

When reviewers disagree by >2 points on any dimension, explain in your note which
reviewer's assessment is more substantive and why. Do not simply average conflicting scores."""

        # Format reviews — compact summary only
        reviews_summary = self._format_reviews_compact(reviews)
        overall_avg = sum(r["average"] for r in reviews) / len(reviews)

        # Trajectory — overall + per-dimension
        trajectory = ""
        if previous_rounds:
            scores_line = [f"R{pr['round']}={pr.get('overall_average', 0):.1f}" for pr in previous_rounds]
            scores_line.append(f"R{round_number}={overall_avg:.1f}")
            trajectory = f"\nTrajectory: {' → '.join(scores_line)}"

            # Per-dimension comparison (last round vs current)
            prev_reviews = previous_rounds[-1].get("reviews", [])
            if prev_reviews:
                dims = ["accuracy", "completeness", "clarity", "novelty", "rigor", "citations"]
                prev_avgs = {}
                curr_avgs = {}
                for d in dims:
                    prev_vals = [r["scores"].get(d, 0) for r in prev_reviews if "scores" in r and not r.get("on_leave")]
                    curr_vals = [r["scores"].get(d, 0) for r in reviews if "scores" in r and not r.get("on_leave")]
                    if prev_vals:
                        prev_avgs[d] = sum(prev_vals) / len(prev_vals)
                    if curr_vals:
                        curr_avgs[d] = sum(curr_vals) / len(curr_vals)
                deltas = []
                for d in dims:
                    if d in prev_avgs and d in curr_avgs:
                        delta = curr_avgs[d] - prev_avgs[d]
                        flag = " ⚠" if abs(delta) < 0.5 and curr_avgs[d] < 6 else ""
                        deltas.append(f"{d[:3]}: {prev_avgs[d]:.0f}→{curr_avgs[d]:.0f} ({delta:+.1f}){flag}")
                if deltas:
                    trajectory += f"\nDimension changes: {' | '.join(deltas)}"

        # Flags
        flags = ""
        if completeness_warning:
            flags += f"\n⚠ INCOMPLETE: {completeness_warning}"
        if outlier_info:
            flags += f"\n⚠ OUTLIER: {outlier_info}"

        final_round = round_number >= max_rounds
        decision_options = "ACCEPT or REJECT" if final_round else "ACCEPT, MINOR_REVISION, MAJOR_REVISION, or REJECT"

        prompt = f"""Round {round_number}/{max_rounds} | Avg score: {overall_avg:.1f}/10 | Threshold: {threshold}{trajectory}
{"⚠ FINAL ROUND — binary decision only (ACCEPT or REJECT)." if final_round else ""}
{flags}

REVIEWS:
{reviews_summary}

Respond with JSON only:

{{
  "decision": "{decision_options}",
  "confidence": <1-5>,
  "note": "<1-3 sentences: key rationale for your decision>",
  "required_changes": ["<change>", "..."]
}}

required_changes: list specific changes if requesting revision; empty list [] if accepting or rejecting."""

        response = await self.llm.generate(
            prompt=prompt,
            system=system_prompt,
            temperature=0.3,
            max_tokens=1024
        )

        # Parse JSON response
        import json
        import re
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        decision_data = None
        try:
            decision_data = json.loads(content)
        except json.JSONDecodeError:
            json_match = re.search(r'```json\s*\n(.*?)\n```', response.content, re.DOTALL)
            if json_match:
                try:
                    decision_data = json.loads(json_match.group(1).strip())
                except json.JSONDecodeError:
                    pass

            if decision_data is None:
                brace_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if brace_match:
                    try:
                        decision_data = json.loads(brace_match.group(0))
                    except json.JSONDecodeError:
                        pass

            if decision_data is None:
                raise ValueError(
                    f"Failed to parse moderator decision as JSON\n"
                    f"Content preview: {content[:200]}..."
                )

        # Add metadata
        decision_data["round"] = round_number
        decision_data["overall_average"] = round(overall_avg, 1)
        decision_data["tokens"] = response.total_tokens
        decision_data["input_tokens"] = response.input_tokens or 0
        decision_data["output_tokens"] = response.output_tokens or 0
        decision_data["model"] = self.model

        return decision_data

    def _format_reviews_compact(self, reviews: List[Dict]) -> str:
        """Format reviews as compact summary for moderator."""
        parts = []
        for i, review in enumerate(reviews, 1):
            scores = review["scores"]
            score_str = " | ".join(f"{k[:3]}={v}" for k, v in scores.items())
            weaknesses = "\n    - ".join(review.get("weaknesses", []))
            if weaknesses:
                weaknesses = "    - " + weaknesses
            # Include detailed_feedback summary (first 300 chars)
            detailed = review.get("detailed_feedback", "")
            detail_summary = detailed[:300].rstrip()
            if len(detailed) > 300:
                detail_summary += "..."
            parts.append(
                f"R{i} ({review['specialist_name']}): avg={review['average']}/10 [{score_str}]\n"
                f"  Summary: {review['summary']}\n"
                f"  Weaknesses:\n{weaknesses}\n"
                f"  Analysis: {detail_summary}"
            )
        return "\n".join(parts)
