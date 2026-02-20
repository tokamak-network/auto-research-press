"""Desk editor agent for initial manuscript screening (desk reject)."""

from typing import Optional

from ..model_config import create_llm_for_role


class DeskEditorAgent:
    """Lightweight editor that screens manuscripts before full peer review.

    Acts as a journal editor performing an initial desk screening to catch
    manuscripts with obvious fatal flaws, saving the cost of full multi-expert
    peer review. Uses a cheap, fast model (Haiku) with a short prompt.
    """

    def __init__(self, role: str = "desk_editor"):
        """Initialize desk editor agent.

        Args:
            role: Role name for model config lookup
        """
        self.llm = create_llm_for_role(role)
        self.model = self.llm.model

    async def screen(self, manuscript: str, topic: str, category: Optional[str] = None) -> dict:
        """Screen a manuscript for obvious fatal flaws.

        Args:
            manuscript: The manuscript text to screen
            topic: The intended research topic
            category: Human-readable academic category (e.g. "Computer Science (Theory & Algorithms)")

        Returns:
            Dictionary with decision, reason, and token count:
            {"decision": "PASS"|"DESK_REJECT", "reason": "...", "tokens": N}
        """
        system_prompt = (
            "You are a journal editor performing a quick desk screening. "
            "Decide whether a manuscript should proceed to full peer review "
            "or be desk-rejected for obvious fatal flaws. "
            "Be lenient: only reject manuscripts with clear, undeniable problems. "
            "When in doubt, PASS."
        )

        category_line = ""
        category_check = ""
        if category:
            category_line = f'\nAssigned academic field: "{category}"\n'
            category_check = (
                "5. The manuscript's actual subject matter clearly belongs to a "
                "completely different academic field than the assigned field "
                "(e.g. a biology paper assigned to Computer Science)\n"
            )

        prompt = f"""Screen this manuscript submitted for the topic: "{topic}"
{category_line}
MANUSCRIPT (first 3000 chars):
{manuscript[:3000]}

---

Desk-reject ONLY if ANY of these apply:
1. Content is completely unrelated to the stated topic
2. Manuscript is extremely short or lacks any structure (no sections/headings)
3. Text is meaningless, garbled, or clearly non-academic (e.g. lorem ipsum)
4. Critical sections are entirely missing (no introduction AND no analysis AND no conclusion)
{category_check}
If the manuscript has reasonable content related to the topic, PASS it.

Respond in JSON:
{{"decision": "PASS" or "DESK_REJECT", "reason": "<one sentence explanation>"}}"""

        response = await self.llm.generate(
            prompt=prompt,
            system=system_prompt,
            temperature=0.1,
            max_tokens=512,
            json_mode=True
        )

        # Parse JSON response
        from ..utils.json_repair import repair_json
        try:
            result = repair_json(response.content)
        except ValueError:
            # If parsing fails, default to PASS (don't block on parse errors)
            result = {
                "decision": "PASS",
                "reason": "Desk screening parse error; defaulting to pass."
            }

        # Normalize decision
        decision = result.get("decision", "PASS").upper().strip()
        if decision not in ("PASS", "DESK_REJECT"):
            decision = "PASS"

        return {
            "decision": decision,
            "reason": result.get("reason", ""),
            "tokens": response.total_tokens,
            "input_tokens": response.input_tokens or 0,
            "output_tokens": response.output_tokens or 0,
            "model": self.model,
        }
