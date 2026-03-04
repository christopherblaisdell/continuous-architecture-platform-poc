#!/usr/bin/env python3
"""
*** DATA ISOLATION NOTICE ***
This script is a LOCAL measurement tool that reads ONLY from the local git
repository and local JSON snapshot files. It makes NO network calls, uses
NO API credentials, and accesses NO corporate systems.

Cost Measurement Tool for Continuous Architecture Platform
==========================================================
Captures baseline/post-execution workspace snapshots, calculates content
deltas, estimates token consumption, and produces cost reports comparing
fixed (GitHub Copilot) and variable (OpenRouter) pricing models.

Usage:
    python scripts/cost-measurement.py baseline              # Before scenarios
    python scripts/cost-measurement.py measure               # After scenarios
    python scripts/cost-measurement.py report                # Produce cost report
    python scripts/cost-measurement.py report --format=csv   # CSV output
    python scripts/cost-measurement.py analyze <sha1> <sha2> # Analyze commit range
"""

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_DIR = WORKSPACE_ROOT / "scripts" / "snapshots"
WORKSPACE_SUBDIR = "phase-1-ai-tool-cost-comparison/workspace"

# Token estimation: ~4 characters per token for English prose/code mix
CHARS_PER_TOKEN = 4

# Pricing models
COPILOT_BUSINESS_MONTHLY = 19.00   # USD / seat / month
COPILOT_ENTERPRISE_MONTHLY = 39.00  # USD / seat / month

# OpenRouter pricing (Claude Opus 4.6 via OpenRouter, as of 2026)
# NOTE: These are estimates. Actual costs come from OpenRouter Activity page.
# Check https://openrouter.ai/models for current pricing.
OPENROUTER_INPUT_PRICE_PER_1M = 15.00    # USD per 1M input tokens (Claude Opus 4.6)
OPENROUTER_OUTPUT_PRICE_PER_1M = 75.00   # USD per 1M output tokens (Claude Opus 4.6)

# Scenario metadata from measurement protocol
SCENARIOS = {
    "SC-01": {"ticket": "NTK-10005", "name": "New Ticket Triage",        "complexity": "Low",       "monthly_freq": 10, "max_score": 25},
    "SC-02": {"ticket": "NTK-10002", "name": "Solution Design",          "complexity": "Medium",    "monthly_freq":  6, "max_score": 35},
    "SC-03": {"ticket": "NTK-10004", "name": "Investigation Analysis",   "complexity": "High",      "monthly_freq":  4, "max_score": 30},
    "SC-04": {"ticket": "NTK-10001", "name": "Architecture Update",      "complexity": "Medium",    "monthly_freq":  4, "max_score": 25},
    "SC-05": {"ticket": "NTK-10003", "name": "Complex Cross-Service",    "complexity": "Very High", "monthly_freq":  2, "max_score": 40},
}

TOTAL_MONTHLY_RUNS = sum(s["monthly_freq"] for s in SCENARIOS.values())  # 26

# File extensions to measure
MEASURABLE_EXTENSIONS = {".md", ".yaml", ".yml", ".py", ".java", ".puml", ".json", ".xml", ".txt"}


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def git(*args):
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=WORKSPACE_ROOT
    )
    if result.returncode != 0:
        print(f"git error: {result.stderr.strip()}", file=sys.stderr)
    return result.stdout.strip()


def current_sha():
    return git("rev-parse", "HEAD")


def current_branch():
    return git("rev-parse", "--abbrev-ref", "HEAD")


def diff_stat(sha_from, sha_to):
    """Return (files_changed, insertions, deletions) between two commits."""
    raw = git("diff", "--shortstat", f"{sha_from}..{sha_to}")
    files = ins = dels = 0
    for part in raw.split(","):
        part = part.strip()
        if "file" in part:
            files = int(part.split()[0])
        elif "insertion" in part:
            ins = int(part.split()[0])
        elif "deletion" in part:
            dels = int(part.split()[0])
    return files, ins, dels


def added_content_bytes(sha_from, sha_to):
    """Count bytes of added lines (lines starting with + but not ++) in diff."""
    diff = git("diff", f"{sha_from}..{sha_to}")
    total = 0
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            total += len(line) - 1  # subtract the leading '+'
    return total


def removed_content_bytes(sha_from, sha_to):
    """Count bytes of removed lines (lines starting with - but not --) in diff."""
    diff = git("diff", f"{sha_from}..{sha_to}")
    total = 0
    for line in diff.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            total += len(line) - 1
    return total


def per_scenario_added_bytes(sha_from, sha_to):
    """Break down added bytes by scenario ticket."""
    # Map of glob patterns per scenario
    scenario_patterns = {
        "SC-01": ["*NTK-10005*", "*ntk10005*"],
        "SC-02": ["*NTK-10002*", "*ntk10002*"],
        "SC-03": ["*NTK-10004*", "*ntk10004*"],
        "SC-04": ["*NTK-10001*", "*ntk10001*", "*svc-trail-management*"],
        "SC-05": ["*NTK-10003*", "*ntk10003*", "*novatrek-component*"],
    }
    results = {}
    for sc_id, patterns in scenario_patterns.items():
        diff = git("diff", f"{sha_from}..{sha_to}", "--", *patterns)
        total = 0
        for line in diff.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                total += len(line) - 1
        results[sc_id] = total
    return results


# ---------------------------------------------------------------------------
# Workspace inventory
# ---------------------------------------------------------------------------

def workspace_inventory():
    """Return dict of {relative_path: {size, sha256}} for measurable files."""
    ws_path = WORKSPACE_ROOT / WORKSPACE_SUBDIR
    inventory = {}
    if not ws_path.exists():
        ws_path = WORKSPACE_ROOT  # Fall back to full repo
    for root, _, files in os.walk(ws_path):
        for name in files:
            fpath = Path(root) / name
            if fpath.suffix.lower() not in MEASURABLE_EXTENSIONS:
                continue
            rel = fpath.relative_to(WORKSPACE_ROOT)
            try:
                data = fpath.read_bytes()
                inventory[str(rel)] = {
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            except (PermissionError, OSError):
                pass
    return inventory


def inventory_summary(inv):
    """Return (file_count, total_bytes) for an inventory dict."""
    return len(inv), sum(v["size"] for v in inv.values())


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------

def estimate_tokens(char_count):
    """Estimate token count from character count (~4 chars/token)."""
    return max(1, char_count // CHARS_PER_TOKEN)


# ---------------------------------------------------------------------------
# Cost calculation
# ---------------------------------------------------------------------------

def copilot_cost_per_run(monthly_price, runs_per_month):
    """Amortized cost per scenario run under fixed pricing."""
    return monthly_price / runs_per_month if runs_per_month > 0 else 0.0


def openrouter_cost(input_tokens, output_tokens):
    """Variable cost estimate for a single run through OpenRouter."""
    input_cost = (input_tokens / 1_000_000) * OPENROUTER_INPUT_PRICE_PER_1M
    output_cost = (output_tokens / 1_000_000) * OPENROUTER_OUTPUT_PRICE_PER_1M
    return input_cost + output_cost


def openrouter_monthly_cost(scenario_costs):
    """Total monthly variable cost across all scenarios."""
    total = 0.0
    for sc_id, cost in scenario_costs.items():
        freq = SCENARIOS[sc_id]["monthly_freq"]
        total += cost * freq
    return total


# ---------------------------------------------------------------------------
# Snapshot management
# ---------------------------------------------------------------------------

def save_snapshot(name, data):
    """Save a snapshot to the snapshots directory."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Snapshot saved: {path}")
    return path


def load_snapshot(name):
    """Load a snapshot from the snapshots directory."""
    path = SNAPSHOT_DIR / f"{name}.json"
    if not path.exists():
        print(f"Snapshot not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def capture_snapshot():
    """Capture current workspace state as a snapshot dict."""
    inv = workspace_inventory()
    file_count, total_bytes = inventory_summary(inv)
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_sha": current_sha(),
        "git_branch": current_branch(),
        "file_count": file_count,
        "total_bytes": total_bytes,
        "inventory": inv,
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_baseline(_args):
    """Capture baseline snapshot before scenario execution."""
    print("Capturing baseline snapshot...")
    snap = capture_snapshot()
    save_snapshot("baseline", snap)
    print(f"  Git SHA:    {snap['git_sha'][:10]}")
    print(f"  Files:      {snap['file_count']}")
    print(f"  Total size: {snap['total_bytes']:,} bytes")
    print(f"  Estimated context tokens: ~{estimate_tokens(snap['total_bytes']):,}")


def cmd_measure(_args):
    """Capture post-execution snapshot and calculate delta."""
    print("Capturing post-execution snapshot...")
    snap = capture_snapshot()
    save_snapshot("post-execution", snap)

    # Load baseline if it exists
    baseline_path = SNAPSHOT_DIR / "baseline.json"
    if baseline_path.exists():
        baseline = load_snapshot("baseline")
        print("\n--- Delta from Baseline ---")
        delta_files = snap["file_count"] - baseline["file_count"]
        delta_bytes = snap["total_bytes"] - baseline["total_bytes"]

        sha_from = baseline["git_sha"]
        sha_to = snap["git_sha"]
        files_changed, ins, dels = diff_stat(sha_from, sha_to)
        added_bytes = added_content_bytes(sha_from, sha_to)
        removed_bytes = removed_content_bytes(sha_from, sha_to)

        print(f"  Baseline SHA:      {sha_from[:10]}")
        print(f"  Current SHA:       {sha_to[:10]}")
        print(f"  New files:         {delta_files:+d}")
        print(f"  Size delta:        {delta_bytes:+,} bytes")
        print(f"  Git files changed: {files_changed}")
        print(f"  Lines added:       {ins:,}")
        print(f"  Lines removed:     {dels:,}")
        print(f"  Added content:     {added_bytes:,} bytes")
        print(f"  Removed content:   {removed_bytes:,} bytes")
        print(f"  Est. output tokens: ~{estimate_tokens(added_bytes):,}")
        print(f"  Est. input tokens:  ~{estimate_tokens(snap['total_bytes']):,}")

        # Save delta
        delta = {
            "baseline_sha": sha_from,
            "current_sha": sha_to,
            "baseline_timestamp": baseline["timestamp"],
            "current_timestamp": snap["timestamp"],
            "delta_files": delta_files,
            "delta_bytes": delta_bytes,
            "files_changed": files_changed,
            "lines_added": ins,
            "lines_removed": dels,
            "added_content_bytes": added_bytes,
            "removed_content_bytes": removed_bytes,
            "est_output_tokens": estimate_tokens(added_bytes),
            "est_input_tokens": estimate_tokens(snap["total_bytes"]),
        }
        save_snapshot("delta", delta)
    else:
        print("  (No baseline snapshot found — run 'baseline' first for delta)")


def cmd_report(args):
    """Produce a cost comparison report."""
    # Try to load delta, or compute from analyze args
    delta_path = SNAPSHOT_DIR / "delta.json"
    if not delta_path.exists():
        print("No delta snapshot found. Run 'baseline' then 'measure' first,")
        print("or use 'analyze <sha1> <sha2>' to analyze a commit range.")
        sys.exit(1)

    delta = load_snapshot("delta")
    _produce_report(delta, fmt=getattr(args, "format", "text"))


def cmd_analyze(args):
    """Analyze cost for a specific commit range."""
    sha_from = args.sha_from
    sha_to = args.sha_to

    print(f"Analyzing commit range: {sha_from[:10]}..{sha_to[:10]}")

    files_changed, ins, dels = diff_stat(sha_from, sha_to)
    added_bytes = added_content_bytes(sha_from, sha_to)
    removed_bytes = removed_content_bytes(sha_from, sha_to)

    # Get workspace size at sha_to for input estimate
    # Use current workspace size as proxy (close enough for estimation)
    inv = workspace_inventory()
    _, total_bytes = inventory_summary(inv)

    delta = {
        "baseline_sha": sha_from,
        "current_sha": sha_to,
        "files_changed": files_changed,
        "lines_added": ins,
        "lines_removed": dels,
        "added_content_bytes": added_bytes,
        "removed_content_bytes": removed_bytes,
        "est_output_tokens": estimate_tokens(added_bytes),
        "est_input_tokens": estimate_tokens(total_bytes),
    }
    save_snapshot("delta", delta)
    _produce_report(delta, fmt=getattr(args, "format", "text"))


def _produce_report(delta, fmt="text"):
    """Generate the cost comparison report from delta data."""
    output_tokens = delta["est_output_tokens"]
    input_tokens = delta["est_input_tokens"]
    total_tokens = input_tokens + output_tokens

    # --- Per-scenario breakdown ---
    sha_from = delta.get("baseline_sha", "")
    sha_to = delta.get("current_sha", "")
    per_sc = {}
    if sha_from and sha_to:
        per_sc = per_scenario_added_bytes(sha_from, sha_to)

    # --- Cost calculations ---
    copilot_biz_per_run = copilot_cost_per_run(COPILOT_BUSINESS_MONTHLY, TOTAL_MONTHLY_RUNS)
    copilot_ent_per_run = copilot_cost_per_run(COPILOT_ENTERPRISE_MONTHLY, TOTAL_MONTHLY_RUNS)

    # Variable cost for the whole batch (all 5 scenarios once)
    variable_total = openrouter_cost(input_tokens, output_tokens)

    # Per-scenario variable costs (proportional to output bytes)
    sc_variable_costs = {}
    total_sc_bytes = sum(per_sc.values()) if per_sc else 1
    for sc_id in SCENARIOS:
        sc_bytes = per_sc.get(sc_id, 0)
        # Input tokens proportional to output (each scenario reads similar context)
        sc_input = input_tokens // len(SCENARIOS)
        sc_output = estimate_tokens(sc_bytes)
        sc_variable_costs[sc_id] = openrouter_cost(sc_input, sc_output)

    # Monthly projections
    variable_monthly = openrouter_monthly_cost(sc_variable_costs)

    # --- Output ---
    if fmt == "csv":
        _report_csv(delta, per_sc, sc_variable_costs, copilot_biz_per_run,
                     copilot_ent_per_run, variable_total, variable_monthly)
    else:
        _report_text(delta, per_sc, sc_variable_costs, copilot_biz_per_run,
                      copilot_ent_per_run, variable_total, variable_monthly)


def _report_text(delta, per_sc, sc_variable_costs, copilot_biz_per_run,
                  copilot_ent_per_run, variable_total, variable_monthly):
    """Print human-readable cost report."""
    output_tokens = delta["est_output_tokens"]
    input_tokens = delta["est_input_tokens"]

    print("\n" + "=" * 72)
    print("  COST MEASUREMENT REPORT")
    print("  Continuous Architecture Platform — Phase 1 AI Tool Comparison")
    print("=" * 72)
    print(f"\n  Commit Range:  {delta.get('baseline_sha', '?')[:10]}..{delta.get('current_sha', '?')[:10]}")
    print(f"  Files Changed: {delta['files_changed']}")
    print(f"  Lines Added:   {delta['lines_added']:,}")
    print(f"  Lines Removed: {delta['lines_removed']:,}")
    print(f"\n  Estimated Input Tokens:  {input_tokens:>10,}")
    print(f"  Estimated Output Tokens: {output_tokens:>10,}")
    print(f"  Total Tokens:            {input_tokens + output_tokens:>10,}")

    print("\n" + "-" * 72)
    print("  PER-SCENARIO BREAKDOWN")
    print("-" * 72)
    print(f"  {'Scenario':<10} {'Ticket':<12} {'Output Bytes':>13} {'Est Tokens':>11} {'Variable $':>11} {'Fixed Biz $':>12}")
    print(f"  {'─' * 10} {'─' * 12} {'─' * 13} {'─' * 11} {'─' * 11} {'─' * 12}")

    for sc_id, meta in SCENARIOS.items():
        sc_bytes = per_sc.get(sc_id, 0)
        sc_tokens = estimate_tokens(sc_bytes)
        sc_var = sc_variable_costs.get(sc_id, 0.0)
        print(f"  {sc_id:<10} {meta['ticket']:<12} {sc_bytes:>13,} {sc_tokens:>11,} ${sc_var:>10.4f} ${copilot_biz_per_run:>11.4f}")

    # Overhead (results doc, ADR updates, etc.)
    accounted = sum(per_sc.values())
    total_added = delta["added_content_bytes"]
    overhead = total_added - accounted
    if overhead > 0:
        print(f"  {'Overhead':<10} {'(results)':<12} {overhead:>13,} {estimate_tokens(overhead):>11,}       —            —")

    print(f"\n  {'TOTAL':<10} {'':12} {total_added:>13,} {delta['est_output_tokens']:>11,} ${variable_total:>10.4f}")

    print("\n" + "-" * 72)
    print("  MONTHLY COST PROJECTION (26 runs/month)")
    print("-" * 72)
    print(f"  OpenRouter (variable):          ${variable_monthly:>8.2f} /month")
    print(f"  GitHub Copilot Business (fixed): ${COPILOT_BUSINESS_MONTHLY:>8.2f} /month")
    print(f"  GitHub Copilot Enterprise (fixed):${COPILOT_ENTERPRISE_MONTHLY:>7.2f} /month")
    print(f"\n  Copilot Business per-run amortized:  ${copilot_biz_per_run:.4f}")
    print(f"  Copilot Enterprise per-run amortized: ${copilot_ent_per_run:.4f} (per {TOTAL_MONTHLY_RUNS} runs)")

    # Break-even analysis
    if variable_total > 0:
        break_even_biz = COPILOT_BUSINESS_MONTHLY / (variable_monthly / TOTAL_MONTHLY_RUNS) if variable_monthly > 0 else float("inf")
        break_even_ent = COPILOT_ENTERPRISE_MONTHLY / (variable_monthly / TOTAL_MONTHLY_RUNS) if variable_monthly > 0 else float("inf")
        print(f"\n  Break-even runs/month (Copilot vs Variable):")
        print(f"    Business:   {break_even_biz:>6.1f} runs (current: {TOTAL_MONTHLY_RUNS})")
        print(f"    Enterprise: {break_even_ent:>6.1f} runs (current: {TOTAL_MONTHLY_RUNS})")

    print("\n" + "=" * 72)
    print("  PRICING ASSUMPTIONS")
    print("=" * 72)
    print(f"  Token estimation:     ~{CHARS_PER_TOKEN} characters per token")
    print(f"  OpenRouter input pricing:   ${OPENROUTER_INPUT_PRICE_PER_1M:.2f} / 1M tokens")
    print(f"  OpenRouter output pricing:  ${OPENROUTER_OUTPUT_PRICE_PER_1M:.2f} / 1M tokens")
    print(f"  Copilot Business:     ${COPILOT_BUSINESS_MONTHLY:.2f} / seat / month")
    print(f"  Copilot Enterprise:   ${COPILOT_ENTERPRISE_MONTHLY:.2f} / seat / month")
    print(f"  Monthly run volume:   {TOTAL_MONTHLY_RUNS} runs across {len(SCENARIOS)} scenarios")
    print()


def _report_csv(delta, per_sc, sc_variable_costs, copilot_biz_per_run,
                 copilot_ent_per_run, variable_total, variable_monthly):
    """Print CSV cost report."""
    print("scenario,ticket,complexity,monthly_freq,output_bytes,est_output_tokens,variable_cost_usd,copilot_biz_amortized_usd,copilot_ent_amortized_usd")
    for sc_id, meta in SCENARIOS.items():
        sc_bytes = per_sc.get(sc_id, 0)
        sc_tokens = estimate_tokens(sc_bytes)
        sc_var = sc_variable_costs.get(sc_id, 0.0)
        print(f"{sc_id},{meta['ticket']},{meta['complexity']},{meta['monthly_freq']},{sc_bytes},{sc_tokens},{sc_var:.6f},{copilot_biz_per_run:.6f},{copilot_ent_per_run:.6f}")
    print(f"TOTAL,,,,{delta['added_content_bytes']},{delta['est_output_tokens']},{variable_total:.6f},{COPILOT_BUSINESS_MONTHLY:.2f},{COPILOT_ENTERPRISE_MONTHLY:.2f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Cost measurement tool for AI architecture scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("baseline", help="Capture baseline snapshot before scenarios")
    sub.add_parser("measure", help="Capture post-execution snapshot and calculate delta")

    report_p = sub.add_parser("report", help="Produce cost comparison report")
    report_p.add_argument("--format", choices=["text", "csv"], default="text",
                          help="Output format (default: text)")

    analyze_p = sub.add_parser("analyze", help="Analyze a specific commit range")
    analyze_p.add_argument("sha_from", help="Starting commit SHA")
    analyze_p.add_argument("sha_to", help="Ending commit SHA")
    analyze_p.add_argument("--format", choices=["text", "csv"], default="text",
                           help="Output format (default: text)")

    args = parser.parse_args()

    commands = {
        "baseline": cmd_baseline,
        "measure": cmd_measure,
        "report": cmd_report,
        "analyze": cmd_analyze,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
