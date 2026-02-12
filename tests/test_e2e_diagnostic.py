#!/usr/bin/env python3
"""End-to-end diagnostic: generate one article and quantify quality per phase.

Usage:
    # Default (professional, survey, short, 2 rounds, threshold 7.0)
    python3 tests/test_e2e_diagnostic.py

    # Custom
    python3 tests/test_e2e_diagnostic.py --topic "Quantum computing" --audience professional --rounds 2
    python3 tests/test_e2e_diagnostic.py --all-audiences
    python3 tests/test_e2e_diagnostic.py --topic "..." --audience beginner --research-type explainer
    python3 tests/test_e2e_diagnostic.py --threshold 6.0 --num-coauthors 3 --num-experts 4
"""

import argparse
import asyncio
import json
import io
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# Ensure project root is on path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# stderr handle for progress output (survives stdout redirect)
_stderr = sys.stderr


def _progress(audience: str, message: str):
    """Print tagged progress line to stderr."""
    tag = f"\033[1m[{audience:>14}]\033[0m"
    _stderr.write(f"  {tag} {message}\n")
    _stderr.flush()


# ── Diagnostic check helpers ────────────────────────────────────────────────

class Check:
    """Single diagnostic check result."""
    def __init__(self, name: str, value, status: str, detail: str = ""):
        self.name = name
        self.value = value
        self.status = status  # PASS / WARN / FAIL
        self.detail = detail

    def to_dict(self):
        return {"name": self.name, "value": self.value, "status": self.status, "detail": self.detail}


def _status(value, pass_fn, warn_fn) -> str:
    if pass_fn(value):
        return "PASS"
    if warn_fn(value):
        return "WARN"
    return "FAIL"


STATUS_ICONS = {"PASS": "\033[32mPASS\033[0m", "WARN": "\033[33mWARN\033[0m", "FAIL": "\033[31mFAIL\033[0m"}


# ── Phase diagnostics ──────────────────────────────────────────────────────

def diagnose_research(research_notes: dict) -> list[Check]:
    """Phase 1: Research quality checks."""
    checks = []
    refs = research_notes.get("references", [])
    findings = research_notes.get("findings", [])

    # Reference count
    ref_count = len(refs)
    checks.append(Check(
        "ref_count", ref_count,
        _status(ref_count, lambda v: v >= 8, lambda v: v >= 4),
        f"{ref_count} references"
    ))

    # Finding count
    finding_count = len(findings)
    checks.append(Check(
        "finding_count", finding_count,
        _status(finding_count, lambda v: v >= 4, lambda v: v >= 2),
        f"{finding_count} findings"
    ))

    # Source diversity (check URLs for known sources)
    source_types = set()
    for ref in refs:
        url = ref.get("url", "") or ""
        if "openalex" in url:
            source_types.add("OpenAlex")
        elif "arxiv" in url:
            source_types.add("arXiv")
        elif "semanticscholar" in url or "api.semanticscholar" in url:
            source_types.add("S2")
        elif url:
            source_types.add("Brave/Other")
    diversity = len(source_types)
    checks.append(Check(
        "source_diversity", diversity,
        _status(diversity, lambda v: v >= 2, lambda v: v >= 1),
        f"{diversity}/4 source types ({', '.join(sorted(source_types)) or 'none'})"
    ))

    return checks


def diagnose_plan(manuscript_data: dict, target_length: int, article_length: str, research_notes: dict) -> list[Check]:
    """Phase 2 (plan): Section structure and reference allocation checks."""
    checks = []
    sections = manuscript_data.get("sections", [])
    all_ref_ids = {r.get("id") or r.get("ref_id") for r in research_notes.get("references", [])}

    # Section count
    sec_count = len(sections)
    if article_length == "short":
        checks.append(Check(
            "section_count", sec_count,
            _status(sec_count, lambda v: 3 <= v <= 5, lambda v: 2 <= v <= 6),
            f"{sec_count} sections (target: 3-5 for short)"
        ))
    else:
        checks.append(Check(
            "section_count", sec_count,
            _status(sec_count, lambda v: 5 <= v <= 7, lambda v: 4 <= v <= 8),
            f"{sec_count} sections (target: 5-7 for full)"
        ))

    # Length budget sum vs target
    budget_sum = sum(s.get("target_length", 0) for s in sections)
    if target_length > 0:
        ratio = budget_sum / target_length
        checks.append(Check(
            "length_budget", budget_sum,
            _status(ratio, lambda v: 0.9 <= v <= 1.1, lambda v: 0.7 <= v <= 1.3),
            f"{budget_sum}/{target_length} words ({ratio:.0%})"
        ))

    # Reference assignment rate
    sections_with_refs = sum(1 for s in sections if s.get("relevant_references"))
    if sec_count > 0:
        assignment_rate = sections_with_refs / sec_count
        checks.append(Check(
            "ref_assignment", sections_with_refs,
            _status(assignment_rate, lambda v: v >= 1.0, lambda v: v >= 0.5),
            f"{sections_with_refs}/{sec_count} sections have refs"
        ))

    # Unused references (refs not assigned to any section)
    assigned_refs = set()
    for s in sections:
        assigned_refs.update(s.get("relevant_references", []))
    unused = all_ref_ids - assigned_refs
    if all_ref_ids:
        unused_rate = len(unused) / len(all_ref_ids)
        checks.append(Check(
            "unused_refs", len(unused),
            _status(unused_rate, lambda v: v < 0.2, lambda v: v <= 0.5),
            f"{len(unused)}/{len(all_ref_ids)} refs unused ({unused_rate:.0%})"
        ))

    return checks


def diagnose_writing(manuscript: dict, target_length: int, research_notes: dict, audience_level: str) -> list[Check]:
    """Phase 2 (writing): Content quality checks."""
    checks = []
    content = manuscript.get("content", "")
    references_text = manuscript.get("references", "")

    # Word count
    word_count = manuscript.get("word_count", 0) or len(content.split())
    if target_length > 0:
        ratio = word_count / target_length
        deviation = abs(ratio - 1.0)
        checks.append(Check(
            "word_count", word_count,
            _status(deviation, lambda v: v <= 0.2, lambda v: v <= 0.4),
            f"{word_count}/{target_length} words ({ratio:+.0%})"
        ))

    # Inline citation count (extract from content)
    from research_cli.utils.citation_manager import CitationManager
    cited_ids = CitationManager.extract_citations(content)
    inline_count = len(cited_ids)
    checks.append(Check(
        "inline_citations", inline_count,
        _status(inline_count, lambda v: v >= 5, lambda v: v >= 2),
        f"{inline_count} inline citations"
    ))

    # Citation-reference matching (broad pool: research_notes + References section)
    all_known_ref_ids = set()
    for ref in research_notes.get("references", []):
        all_known_ref_ids.add(ref.get("id"))
    ref_pattern = re.findall(r'^\[(\d+)\]', references_text, re.MULTILINE)
    for r in ref_pattern:
        all_known_ref_ids.add(int(r))

    if cited_ids:
        matched = sum(1 for cid in cited_ids if cid in all_known_ref_ids)
        match_rate = matched / len(cited_ids)
        checks.append(Check(
            "citation_match", match_rate,
            _status(match_rate, lambda v: v >= 1.0, lambda v: v >= 0.8),
            f"{matched}/{len(cited_ids)} citations matched ({match_rate:.0%})"
        ))

    # Ghost references (in References section but never cited in body)
    # Only count refs actually listed in the manuscript's References section,
    # NOT all research_notes refs (those are the "available pool", not the output).
    refs_in_output = set()
    for r in ref_pattern:
        refs_in_output.add(int(r))
    if refs_in_output:
        ghost_count = len(refs_in_output - set(cited_ids))
        ghost_rate = ghost_count / len(refs_in_output)
        checks.append(Check(
            "ghost_refs", ghost_count,
            _status(ghost_rate, lambda v: v <= 0.3, lambda v: v <= 0.5),
            f"{ghost_count}/{len(refs_in_output)} refs uncited ({ghost_rate:.0%})"
        ))

    # Audience tone checks
    abstract = manuscript.get("abstract", "")
    checks.extend(_diagnose_audience_tone(content, audience_level, abstract=abstract))

    return checks


def _diagnose_audience_tone(content: str, audience_level: str, abstract: str = "") -> list[Check]:
    """Audience-specific tone verification."""
    checks = []
    # Combine content and abstract for full-text checks
    full_text = content + "\n" + abstract if abstract else content
    bullet_count = len(re.findall(r'^[\s]*[-*]\s', full_text, re.MULTILINE))
    blockquote_count = len(re.findall(r'^>', content, re.MULTILINE))
    key_takeaway_count = content.lower().count("key takeaway")

    if audience_level == "beginner":
        accessible_signals = blockquote_count + key_takeaway_count
        checks.append(Check(
            "beginner_bullets", bullet_count,
            _status(bullet_count, lambda v: v >= 5, lambda v: v >= 3),
            f"{bullet_count} bullet points"
        ))
        checks.append(Check(
            "beginner_callouts", accessible_signals,
            _status(accessible_signals, lambda v: v >= 2, lambda v: v >= 1),
            f"{accessible_signals} callouts/key-takeaways"
        ))
        has_tldr = bool(re.search(r'(TL;DR|Key Takeaway)', full_text, re.IGNORECASE))
        checks.append(Check(
            "beginner_tldr", has_tldr,
            "PASS" if has_tldr else "WARN",
            "TL;DR present" if has_tldr else "No TL;DR section"
        ))
    elif audience_level == "intermediate":
        checks.append(Check(
            "intermediate_bullets", bullet_count,
            _status(bullet_count, lambda v: v >= 3, lambda v: v >= 1),
            f"{bullet_count} bullet points"
        ))
        has_tldr = bool(re.search(r'(TL;DR|Key Takeaway)', full_text, re.IGNORECASE))
        checks.append(Check(
            "intermediate_tldr", has_tldr,
            "PASS" if has_tldr else "WARN",
            "TL;DR present" if has_tldr else "No TL;DR section"
        ))
    else:  # professional
        checks.append(Check(
            "professional_tone", bullet_count,
            _status(bullet_count, lambda v: v <= 5, lambda v: v <= 8),
            f"{bullet_count} bullet points (academic tone)"
        ))

    return checks


def diagnose_review(workflow_data: dict, max_rounds: int) -> list[Check]:
    """Phase 3: Review quality checks."""
    checks = []
    rounds = workflow_data.get("rounds", [])

    if not rounds:
        checks.append(Check("review_data", 0, "FAIL", "No review rounds found"))
        return checks

    final_round = rounds[-1]
    final_score = final_round.get("overall_average", 0)
    decision = final_round.get("moderator_decision", {}).get("decision", "UNKNOWN")

    checks.append(Check(
        "final_score", final_score,
        _status(final_score, lambda v: v >= 7.0, lambda v: v >= 5.0),
        f"{final_score}/10"
    ))

    checks.append(Check(
        "decision", decision,
        "PASS" if decision == "ACCEPT" else ("WARN" if decision in ("MINOR_REVISION", "REVISE") else "FAIL"),
        decision
    ))

    # Per-criterion scores (averaged across reviewers)
    active_reviews = [r for r in final_round.get("reviews", []) if not r.get("on_leave")]
    if active_reviews:
        for criterion in ("citations", "rigor"):
            values = [r.get("scores", {}).get(criterion, 0) for r in active_reviews if r.get("scores", {}).get(criterion)]
            if values:
                avg = sum(values) / len(values)
                checks.append(Check(
                    f"{criterion}_score", round(avg, 1),
                    _status(avg, lambda v: v >= 6, lambda v: v >= 4),
                    f"{avg:.1f}/10"
                ))

    # Round count
    round_count = len(rounds)
    checks.append(Check(
        "round_count", round_count,
        _status(round_count, lambda v: v <= max_rounds, lambda _: True),
        f"{round_count}/{max_rounds} rounds"
    ))

    return checks


def diagnose_performance(workflow_data: dict) -> dict:
    """Extract performance metrics from workflow data."""
    perf = workflow_data.get("performance", {})
    phase_timings = workflow_data.get("phase_timings", []) or []

    result = {
        "wall_time": perf.get("total_duration", 0),
        "total_tokens": perf.get("total_tokens", 0),
        "estimated_cost": perf.get("estimated_cost", 0),
        "tokens_by_model": perf.get("tokens_by_model", {}),
    }

    # Extract phase durations from phase_timings
    for pt in phase_timings:
        if pt and isinstance(pt, dict):
            phase_name = pt.get("phase", "unknown")
            result[f"phase_{phase_name}"] = pt.get("total_duration", 0)

    # Review phase = total - research - writing (approximate)
    review_duration = perf.get("total_duration", 0)
    for pt in phase_timings:
        if pt and isinstance(pt, dict):
            review_duration -= pt.get("total_duration", 0)
    result["phase_review"] = max(0, review_duration)

    return result


# ── Run workflow ────────────────────────────────────────────────────────────

async def run_workflow(
    topic: str, audience: str, rounds: int, article_length: str = "short",
    research_type: str = "survey", threshold: float = 7.0,
    num_coauthors: int = 2, num_experts: int = 3, auto_accept_team: bool = True,
    quiet: bool = False,
):
    """Run CollaborativeWorkflowOrchestrator and return result + timing."""
    from research_cli.agents.writer_team_composer import WriterTeamComposerAgent
    from research_cli.agents.team_composer import TeamComposerAgent
    from research_cli.categories import suggest_category_from_topic
    from research_cli.model_config import get_reviewer_rotation
    from research_cli.models.author import AuthorRole, WriterTeam
    from research_cli.models.expert import ExpertConfig
    from research_cli.workflow.collaborative_workflow import CollaborativeWorkflowOrchestrator

    def _on_status(phase, progress_val, message):
        _progress(audience, message)

    # Detect category
    category = suggest_category_from_topic(topic)
    major_field = category.get("major", "computer_science")
    subfield = category.get("subfield", "")

    target_length = 2000 if article_length == "short" else 4000

    # Compose writer team
    _progress(audience, "Composing writer team...")
    composer = WriterTeamComposerAgent()
    team_config = await composer.propose_and_format_team(
        topic=topic,
        major_field=major_field,
        subfield=subfield,
        num_coauthors=num_coauthors,
    )

    lead_config = team_config["lead_author"]
    lead_author = AuthorRole(
        id=lead_config["id"], name=lead_config["name"],
        role=lead_config["role"], expertise=lead_config["expertise"],
        focus_areas=lead_config["focus_areas"], model=lead_config["model"],
    )
    coauthors = []
    for ca_cfg in team_config["coauthors"]:
        coauthors.append(AuthorRole(
            id=ca_cfg["id"], name=ca_cfg["name"],
            role=ca_cfg["role"], expertise=ca_cfg["expertise"],
            focus_areas=ca_cfg["focus_areas"], model=ca_cfg["model"],
        ))
    writer_team = WriterTeam(lead_author=lead_author, coauthors=coauthors)

    # Compose reviewer team
    _progress(audience, "Composing reviewer team...")
    reviewer_composer = TeamComposerAgent()
    proposals = await reviewer_composer.propose_team(topic, num_experts)
    rotation = get_reviewer_rotation()

    reviewer_configs = []
    for idx, proposal in enumerate(proposals):
        model_spec = rotation[idx % len(rotation)]
        rc = ExpertConfig(
            id=f"reviewer_{idx + 1}", name=proposal.expert_domain,
            domain=proposal.expert_domain, focus_areas=proposal.focus_areas,
            system_prompt="", provider=model_spec.provider, model=model_spec.model,
        )
        reviewer_configs.append(rc)

    # Setup output dir
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_topic = re.sub(r'[^a-z0-9]+', '-', topic.lower())[:60]
    output_dir = ROOT / "tests" / "results" / f"diag-{safe_topic}-{audience}-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run workflow
    _progress(audience, f"Starting workflow (rounds={rounds}, length={article_length})...")
    orchestrator = CollaborativeWorkflowOrchestrator(
        topic=topic,
        major_field=major_field,
        subfield=subfield,
        writer_team=writer_team,
        reviewer_configs=reviewer_configs,
        output_dir=output_dir,
        max_rounds=rounds,
        threshold=threshold,
        target_manuscript_length=target_length,
        article_length=article_length,
        research_type=research_type,
        audience_level=audience,
        status_callback=_on_status,
        quiet=quiet,
    )

    result = await orchestrator.run()
    _progress(audience, "Workflow complete.")
    return result, output_dir, target_length


# ── Report rendering ────────────────────────────────────────────────────────

def render_report(
    topic: str, audience: str, article_length: str, max_rounds: int, target_length: int,
    research_checks: list[Check], plan_checks: list[Check],
    writing_checks: list[Check], review_checks: list[Check],
    perf: dict, file=None,
):
    """Print formatted diagnostic report."""
    out = file or sys.stdout
    all_checks = research_checks + plan_checks + writing_checks + review_checks
    pass_count = sum(1 for c in all_checks if c.status == "PASS")
    warn_count = sum(1 for c in all_checks if c.status == "WARN")
    fail_count = sum(1 for c in all_checks if c.status == "FAIL")

    overall = "HEALTHY" if fail_count == 0 else "DEGRADED" if fail_count <= 2 else "UNHEALTHY"

    def _line(label: str, value, status: str = "", width: int = 38):
        left = f"  {label}:"
        mid = str(value)
        if status:
            icon = STATUS_ICONS.get(status, status)
            out.write(f"{left:<{width}} {mid:<16} {icon}\n")
        else:
            out.write(f"{left:<{width}} {mid}\n")

    out.write(f"\n{'=' * 56}\n")
    out.write(f"  E2E DIAGNOSTIC REPORT\n")
    out.write(f"{'=' * 56}\n")
    _line("Topic", topic)
    _line("Audience", audience)
    _line("Length", f"{article_length} (target: {target_length} words)")
    _line("Rounds", max_rounds)
    out.write("\n")

    def _section(title: str, checks: list[Check]):
        out.write(f"-- {title} " + "-" * (52 - len(title)) + "\n")
        for c in checks:
            _line(c.name, c.detail or c.value, c.status)
        out.write("\n")

    _section("Phase 1: Research", research_checks)
    _section("Phase 2: Plan", plan_checks)
    _section("Phase 2: Writing", writing_checks)
    _section("Phase 3: Review", review_checks)

    # Performance
    out.write("-- Performance " + "-" * 40 + "\n")
    wall = perf.get("wall_time", 0)
    _line("Wall time", f"{wall:.0f}s ({wall / 60:.1f}m)")
    for key in sorted(perf):
        if key.startswith("phase_"):
            phase_name = key.replace("phase_", "")
            _line(f"  {phase_name}", f"{perf[key]:.0f}s")
    _line("Total tokens", f"{perf.get('total_tokens', 0):,}")
    _line("Estimated cost", f"${perf.get('estimated_cost', 0):.3f}")
    out.write("\n")

    # Summary
    out.write("-- Summary " + "-" * 44 + "\n")
    status_color = "\033[32m" if overall == "HEALTHY" else ("\033[33m" if overall == "DEGRADED" else "\033[31m")
    out.write(f"  PASS: {pass_count}  WARN: {warn_count}  FAIL: {fail_count}\n")
    out.write(f"  Status: {status_color}{overall}\033[0m\n")
    out.write(f"{'=' * 56}\n\n")
    out.flush()


def save_report_json(
    filepath: Path, topic: str, audience: str, target_length: int,
    research_checks: list[Check], plan_checks: list[Check],
    writing_checks: list[Check], review_checks: list[Check],
    perf: dict,
):
    """Save structured diagnostic result as JSON."""
    all_checks = research_checks + plan_checks + writing_checks + review_checks
    pass_count = sum(1 for c in all_checks if c.status == "PASS")
    warn_count = sum(1 for c in all_checks if c.status == "WARN")
    fail_count = sum(1 for c in all_checks if c.status == "FAIL")

    report = {
        "meta": {
            "topic": topic,
            "audience": audience,
            "target_length": target_length,
            "timestamp": datetime.now().isoformat(),
        },
        "research": {c.name: {"value": c.value, "status": c.status, "detail": c.detail} for c in research_checks},
        "plan": {c.name: {"value": c.value, "status": c.status, "detail": c.detail} for c in plan_checks},
        "writing": {c.name: {"value": c.value, "status": c.status, "detail": c.detail} for c in writing_checks},
        "review": {c.name: {"value": c.value, "status": c.status, "detail": c.detail} for c in review_checks},
        "performance": perf,
        "checks": [c.to_dict() for c in all_checks],
        "summary": {
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
            "status": "HEALTHY" if fail_count == 0 else "DEGRADED" if fail_count <= 2 else "UNHEALTHY",
        },
    }

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, default=str)
    _progress(audience, f"Report saved: {filepath.name}")


# ── Diagnostic runner ───────────────────────────────────────────────────────

async def run_diagnostic(
    topic: str, audience: str, max_rounds: int, article_length: str = "short",
    research_type: str = "survey", threshold: float = 7.0,
    num_coauthors: int = 2, num_experts: int = 3, auto_accept_team: bool = True,
    export: bool = True, quiet: bool = False,
) -> dict:
    """Run single diagnostic: workflow + analysis. Returns diagnostic data dict."""
    target_length = 2000 if article_length == "short" else 4000

    _progress(audience, f"Starting (length={article_length}, rounds={max_rounds}, type={research_type})")

    t0 = time.time()
    result, output_dir, target_length = await run_workflow(
        topic, audience, max_rounds, article_length,
        research_type=research_type, threshold=threshold,
        num_coauthors=num_coauthors, num_experts=num_experts,
        auto_accept_team=auto_accept_team, quiet=quiet,
    )
    wall_time = time.time() - t0

    # Load saved artifacts for deeper analysis
    research_notes = result.get("research_notes", {})
    manuscript = result.get("manuscript", {})

    plan_data_path = output_dir / "manuscript_plan.json"
    plan_data = {}
    if plan_data_path.exists():
        with open(plan_data_path) as f:
            plan_data = json.load(f)

    workflow_path = output_dir / "workflow_complete.json"
    workflow_data = {}
    if workflow_path.exists():
        with open(workflow_path) as f:
            workflow_data = json.load(f)

    # Run diagnostics
    research_checks = diagnose_research(research_notes)
    plan_checks = diagnose_plan(plan_data, target_length, article_length, research_notes)
    writing_checks = diagnose_writing(manuscript, target_length, research_notes, audience)
    review_checks = diagnose_review(workflow_data, max_rounds)
    perf = diagnose_performance(workflow_data)
    perf["wall_time"] = wall_time

    # Export to web/data/ + web/articles/
    if export:
        try:
            from export_to_web import export_single_project
            export_single_project(output_dir)
            _progress(audience, "Exported to web/data/")
        except Exception as e:
            _progress(audience, f"Web export failed: {e}")

    # Save JSON
    safe_topic = re.sub(r'[^a-z0-9]+', '-', topic.lower())[:40]
    json_path = ROOT / "tests" / "results" / f"diagnostic_{safe_topic}_{audience}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    save_report_json(
        json_path, topic, audience, target_length,
        research_checks, plan_checks, writing_checks, review_checks, perf,
    )

    all_checks = research_checks + plan_checks + writing_checks + review_checks
    return {
        "audience": audience,
        "article_length": article_length,
        "max_rounds": max_rounds,
        "target_length": target_length,
        "topic": topic,
        "research_checks": research_checks,
        "plan_checks": plan_checks,
        "writing_checks": writing_checks,
        "review_checks": review_checks,
        "perf": perf,
        "pass": sum(1 for c in all_checks if c.status == "PASS"),
        "warn": sum(1 for c in all_checks if c.status == "WARN"),
        "fail": sum(1 for c in all_checks if c.status == "FAIL"),
    }


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="E2E diagnostic for research article generation")
    parser.add_argument("--topic", default="Quantum computing applications in machine learning",
                        help="Research topic")
    parser.add_argument("--audience", choices=["beginner", "intermediate", "professional"],
                        default="professional", help="Target audience")
    parser.add_argument("--rounds", type=int, default=2, help="Max review rounds")
    parser.add_argument("--length", choices=["short", "full"], default="short",
                        help="Article length")
    parser.add_argument("--research-type", choices=["explainer", "survey", "original"],
                        default="survey", help="Research type (default: survey)")
    parser.add_argument("--threshold", type=float, default=7.0,
                        help="Review acceptance threshold (default: 7.0)")
    parser.add_argument("--num-coauthors", type=int, default=2,
                        help="Number of co-authors (default: 2)")
    parser.add_argument("--num-experts", type=int, default=3,
                        help="Number of reviewer experts (default: 3)")
    parser.add_argument("--auto-accept-team", action="store_true", default=True,
                        help="Auto-accept team composition (default: True)")
    parser.add_argument("--no-export", action="store_true",
                        help="Skip exporting results to web/data/")
    parser.add_argument("--all-audiences", action="store_true",
                        help="Run for all 3 audience levels in parallel")
    args = parser.parse_args()

    if args.all_audiences:
        async def _run_all():
            # Redirect stdout to log file — isolates rich console noise
            log_dir = ROOT / "tests" / "results"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"parallel_log_{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
            log_file = open(log_path, "w")
            old_stdout = sys.stdout
            sys.stdout = log_file

            _stderr.write(f"\n  Verbose output → {log_path}\n")
            _stderr.write(f"  Progress tracked below via [audience] tags.\n\n")

            try:
                tasks = [
                    run_diagnostic(
                        args.topic, aud, args.rounds, args.length,
                        research_type=args.research_type, threshold=args.threshold,
                        num_coauthors=args.num_coauthors, num_experts=args.num_experts,
                        auto_accept_team=args.auto_accept_team,
                        export=not args.no_export, quiet=True,
                    )
                    for aud in ("beginner", "intermediate", "professional")
                ]
                return await asyncio.gather(*tasks)
            finally:
                sys.stdout = old_stdout
                log_file.close()

        results = asyncio.run(_run_all())

        # Render all 3 reports to stdout (now restored)
        for r in results:
            render_report(
                r["topic"], r["audience"], r["article_length"],
                r["max_rounds"], r["target_length"],
                r["research_checks"], r["plan_checks"],
                r["writing_checks"], r["review_checks"], r["perf"],
            )

        # Aggregate summary
        totals = {"pass": 0, "warn": 0, "fail": 0}
        for r in results:
            totals["pass"] += r["pass"]
            totals["warn"] += r["warn"]
            totals["fail"] += r["fail"]

        status = "HEALTHY" if totals["fail"] == 0 else "DEGRADED" if totals["fail"] <= 2 else "UNHEALTHY"
        status_color = "\033[32m" if status == "HEALTHY" else ("\033[33m" if status == "DEGRADED" else "\033[31m")
        print(f"{'=' * 56}")
        print(f"  ALL-AUDIENCES SUMMARY (parallel)")
        print(f"  PASS: {totals['pass']}  WARN: {totals['warn']}  FAIL: {totals['fail']}")
        print(f"  Status: {status_color}{status}\033[0m")
        print(f"{'=' * 56}")
        sys.exit(1 if totals["fail"] > 0 else 0)

    else:
        result = asyncio.run(run_diagnostic(
            args.topic, args.audience, args.rounds, args.length,
            research_type=args.research_type, threshold=args.threshold,
            num_coauthors=args.num_coauthors, num_experts=args.num_experts,
            auto_accept_team=args.auto_accept_team,
            export=not args.no_export,
        ))
        render_report(
            result["topic"], result["audience"], result["article_length"],
            result["max_rounds"], result["target_length"],
            result["research_checks"], result["plan_checks"],
            result["writing_checks"], result["review_checks"], result["perf"],
        )
        sys.exit(1 if result["fail"] > 0 else 0)


if __name__ == "__main__":
    main()
