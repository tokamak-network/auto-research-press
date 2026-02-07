"""Desk editor agent for initial manuscript screening (desk reject)."""

import json
from ..llm import ClaudeLLM
from ..config import get_config


class DeskEditorAgent:
    """Lightweight editor that screens manuscripts before full peer review.

    Acts as a journal editor performing an initial desk screening to catch
    manuscripts with obvious fatal flaws, saving the cost of full multi-expert
    peer review. Uses a cheap, fast model (Haiku) with a short prompt.
    """

    def __init__(self, model: str = "claude-haiku-4"):
        """Initialize desk editor agent.

        Args:
            model: Claude model to use (Haiku for cost efficiency)
        """
        config = get_config()
        llm_config = config.get_llm_config("anthropic", model)
        self.llm = ClaudeLLM(
            api_key=llm_config.api_key,
            model=llm_config.model,
            base_url=llm_config.base_url
        )
        self.model = model

    async def screen(self, manuscript: str, topic: str) -> dict:
        """Screen a manuscript for obvious fatal flaws.

        Args:
            manuscript: The manuscript text to screen
            topic: The intended research topic

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

        prompt = f"""Screen this manuscript submitted for the topic: "{topic}"

MANUSCRIPT (first 3000 chars):
{manuscript[:3000]}

---

Desk-reject ONLY if ANY of these apply:
1. Content is completely unrelated to the stated topic
2. Manuscript is extremely short or lacks any structure (no sections/headings)
3. Text is meaningless, garbled, or clearly non-academic (e.g. lorem ipsum)
4. Critical sections are entirely missing (no introduction AND no analysis AND no conclusion)

If the manuscript has reasonable content related to the topic, PASS it.

Respond in JSON:
{{"decision": "PASS" or "DESK_REJECT", "reason": "<one sentence explanation>"}}"""

        response = await self.llm.generate(
            prompt=prompt,
            system=system_prompt,
            temperature=0.1,
            max_tokens=512
        )

        # Parse JSON response
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
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
            "tokens": response.total_tokens
        }
