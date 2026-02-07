# Dynamic Domain Detection + KaTeX Math Rendering

## Tasks
- [x] Add `get_domain_description()` helper to `research_cli/categories.py`
- [x] Move `suggest_category_from_topic()` from `api_server.py` to `research_cli/categories.py`
- [x] Add `category` parameter to `WorkflowOrchestrator.__init__`, compute `domain_desc`
- [x] Pass `domain` to writer, moderator, and planner agents from orchestrator
- [x] Replace hardcoded "blockchain" in `writer.py` system prompt with dynamic `{domain}`
- [x] Replace hardcoded "blockchain" in `moderator.py` system prompt with dynamic `{domain}`
- [x] Replace hardcoded "blockchain" in `research_planner.py` system prompt with dynamic `{domain}`
- [x] Update `api_server.py` to import from categories and pass `category` to orchestrator
- [x] Update `cli.py` to detect category and pass to orchestrator
- [x] Fix `$` escaping in `export_to_web.py` (only escape `${`, not bare `$`)
- [x] Fix `$` escaping in `api_server.py` submit-article endpoint
- [x] Add KaTeX CSS CDN to `export_to_web.py` HTML template
- [x] Add KaTeX JS + auto-render to `export_to_web.py` HTML template
- [x] Add `renderMathInElement()` call after article content injection
- [x] Improve philosophy keyword stems (epistemolog, ontolog, phenomenolog, etc.)
- [x] Verify AST parse on all 8 modified files
- [x] Verify category detection for philosophy, blockchain, physics topics
- [x] Verify export_to_web.py generates articles with KaTeX tags

## Review
All changes implemented and verified. The system now:
1. Detects academic domain from topic keywords and passes it through to all agent prompts
2. Removes hardcoded "blockchain and distributed systems" from writer, moderator, and planner
3. Renders LaTeX math expressions via KaTeX in generated article HTML
4. Fixes `$` escaping that previously prevented math rendering
