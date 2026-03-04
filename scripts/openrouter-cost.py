#!/usr/bin/env python3
"""
OpenRouter Cost Retrieval Tool
==============================
Queries the OpenRouter API to retrieve exact cost data for AI architecture
scenario runs. Supports querying individual generation stats, current credit
balance, and bulk cost summaries.

This script makes REAL network calls to the OpenRouter API.
Requires the OPENROUTER_API_KEY environment variable to be set.

Usage:
    # Check current credit balance and key info
    python3 scripts/openrouter-cost.py balance

    # Get cost for a specific generation by ID
    python3 scripts/openrouter-cost.py generation gen-xxxxxxxxxxxxxxxx

    # Get total cost for multiple generations (space-separated IDs)
    python3 scripts/openrouter-cost.py generations gen-xxx1 gen-xxx2 gen-xxx3

    # Get cost summary from a file of generation IDs (one per line)
    python3 scripts/openrouter-cost.py summary --file generation-ids.txt

    # Get cost summary with CSV output
    python3 scripts/openrouter-cost.py summary --file generation-ids.txt --format csv

    # Get cost summary with JSON output
    python3 scripts/openrouter-cost.py summary --file generation-ids.txt --format json

Environment Variables:
    OPENROUTER_API_KEY  - Your OpenRouter API key (required)
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
KEY_INFO_ENDPOINT = f"{OPENROUTER_API_BASE}/auth/key"
GENERATION_ENDPOINT = f"{OPENROUTER_API_BASE}/generation"

# Rate limiting: be polite to the API
REQUEST_DELAY_SECONDS = 0.25

# Copilot Pro+ pricing for comparison
COPILOT_PRO_PLUS_MONTHLY = 39.00          # USD / month
COPILOT_PRO_PLUS_INCLUDED_REQUESTS = 1500  # Premium requests included
COPILOT_PRO_PLUS_OVERAGE_PER_REQUEST = 0.04  # USD per additional premium request


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def get_api_key():
    """Get the OpenRouter API key from environment."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("ERROR: OPENROUTER_API_KEY environment variable is not set.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Set it with:", file=sys.stderr)
        print("  export OPENROUTER_API_KEY='sk-or-v1-...'", file=sys.stderr)
        sys.exit(1)
    return key


def api_request(url, api_key):
    """Make an authenticated GET request to the OpenRouter API."""
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code} from {url}", file=sys.stderr)
        print(f"  Response: {body[:500]}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"ERROR: Network error accessing {url}: {e.reason}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_balance(args):
    """Show current API key info and credit balance."""
    api_key = get_api_key()
    data = api_request(KEY_INFO_ENDPOINT, api_key)

    if not data:
        sys.exit(1)

    info = data.get("data", data)

    print("=" * 60)
    print("  OPENROUTER ACCOUNT INFO")
    print("=" * 60)
    print(f"  Label:           {info.get('label', 'N/A')}")
    print(f"  Usage (credits):  ${info.get('usage', 0):.6f}")
    print(f"  Limit:           {'$' + str(info.get('limit', 'None')) if info.get('limit') else 'No limit'}")

    limit = info.get("limit")
    usage = info.get("usage", 0)
    if limit is not None:
        remaining = limit - usage
        print(f"  Remaining:       ${remaining:.6f}")

    rate_limit = info.get("rate_limit", {})
    if rate_limit:
        print(f"\n  Rate Limits:")
        print(f"    Requests:      {rate_limit.get('requests', 'N/A')}")
        print(f"    Interval:      {rate_limit.get('interval', 'N/A')}")

    print()


def cmd_generation(args):
    """Get cost details for a single generation."""
    api_key = get_api_key()
    gen_id = args.generation_id

    data = fetch_generation(gen_id, api_key)
    if not data:
        sys.exit(1)

    print_generation_detail(data)


def cmd_generations(args):
    """Get costs for multiple generation IDs."""
    api_key = get_api_key()
    gen_ids = args.generation_ids

    results = fetch_multiple_generations(gen_ids, api_key)
    print_generation_summary(results, fmt="text")


def cmd_summary(args):
    """Get cost summary from a file of generation IDs."""
    api_key = get_api_key()
    fmt = getattr(args, "format", "text")

    # Read IDs from file
    filepath = args.file
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    gen_ids = []
    for line in lines:
        stripped = line.strip()
        # Skip empty lines and comments
        if stripped and not stripped.startswith("#"):
            # Support "gen-xxx  # optional comment" format
            gen_id = stripped.split("#")[0].strip().split()[0]
            gen_ids.append(gen_id)

    if not gen_ids:
        print(f"ERROR: No generation IDs found in {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching {len(gen_ids)} generation(s) from OpenRouter...\n")
    results = fetch_multiple_generations(gen_ids, api_key)
    print_generation_summary(results, fmt=fmt)


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_generation(gen_id, api_key):
    """Fetch a single generation's stats from OpenRouter."""
    url = f"{GENERATION_ENDPOINT}?id={gen_id}"
    return api_request(url, api_key)


def fetch_multiple_generations(gen_ids, api_key):
    """Fetch multiple generations with rate limiting."""
    results = []
    for i, gen_id in enumerate(gen_ids):
        if i > 0:
            time.sleep(REQUEST_DELAY_SECONDS)

        data = fetch_generation(gen_id, api_key)
        if data:
            gen_data = data.get("data", data)
            results.append(gen_data)
        else:
            print(f"  WARNING: Failed to fetch {gen_id}", file=sys.stderr)
            results.append({"id": gen_id, "error": True})

    return results


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_generation_detail(data):
    """Print detailed info for a single generation."""
    gen = data.get("data", data)

    print("=" * 60)
    print("  GENERATION DETAIL")
    print("=" * 60)
    print(f"  ID:               {gen.get('id', 'N/A')}")
    print(f"  Model:            {gen.get('model', 'N/A')}")
    print(f"  Created:          {format_timestamp(gen.get('created_at'))}")

    tokens = gen.get("tokens_prompt", gen.get("prompt_tokens", 0))
    completion = gen.get("tokens_completion", gen.get("completion_tokens", 0))
    total = tokens + completion

    print(f"\n  Tokens:")
    print(f"    Input:          {tokens:,}")
    print(f"    Output:         {completion:,}")
    print(f"    Total:          {total:,}")

    cost = gen.get("total_cost", gen.get("usage", 0))
    if isinstance(cost, dict):
        cost = cost.get("cost", 0)
    print(f"\n  Cost:             ${cost:.6f}")

    native_cost = gen.get("native_tokens_prompt")
    if native_cost is not None:
        print(f"\n  Native Tokens:")
        print(f"    Prompt:         {gen.get('native_tokens_prompt', 0):,}")
        print(f"    Completion:     {gen.get('native_tokens_completion', 0):,}")

    print()


def print_generation_summary(results, fmt="text"):
    """Print summary of multiple generations."""
    if fmt == "json":
        print_summary_json(results)
        return
    if fmt == "csv":
        print_summary_csv(results)
        return

    # Text format
    total_input = 0
    total_output = 0
    total_cost = 0.0
    successful = 0
    failed = 0

    print("-" * 72)
    print(f"  {'#':<4} {'ID':<28} {'Input':>10} {'Output':>10} {'Cost':>12}")
    print(f"  {'─' * 4} {'─' * 28} {'─' * 10} {'─' * 10} {'─' * 12}")

    for i, gen in enumerate(results, 1):
        if gen.get("error"):
            failed += 1
            print(f"  {i:<4} {gen.get('id', '?'):<28} {'ERROR':>10} {'':>10} {'':>12}")
            continue

        successful += 1
        inp = gen.get("tokens_prompt", gen.get("prompt_tokens", 0))
        out = gen.get("tokens_completion", gen.get("completion_tokens", 0))
        cost = extract_cost(gen)

        total_input += inp
        total_output += out
        total_cost += cost

        gen_id = gen.get("id", "?")
        # Truncate ID for display
        display_id = gen_id if len(gen_id) <= 28 else gen_id[:25] + "..."
        print(f"  {i:<4} {display_id:<28} {inp:>10,} {out:>10,} ${cost:>11.6f}")

    print(f"\n  {'─' * 72}")
    print(f"  {'TOTAL':<33} {total_input:>10,} {total_output:>10,} ${total_cost:>11.6f}")
    print(f"  Successful: {successful}  |  Failed: {failed}")

    # Copilot Pro+ comparison
    print(f"\n{'=' * 72}")
    print("  COPILOT PRO+ COMPARISON")
    print("=" * 72)
    print(f"  OpenRouter actual cost (this run):  ${total_cost:.6f}")
    print(f"  Copilot Pro+ base subscription:      ${COPILOT_PRO_PLUS_MONTHLY:.2f}/month")
    print(f"  Copilot Pro+ included requests:      {COPILOT_PRO_PLUS_INCLUDED_REQUESTS}")
    print(f"  Copilot Pro+ overage rate:           ${COPILOT_PRO_PLUS_OVERAGE_PER_REQUEST:.2f}/request")

    # For comparison context:
    total_requests = successful
    if total_requests > COPILOT_PRO_PLUS_INCLUDED_REQUESTS:
        overage_requests = total_requests - COPILOT_PRO_PLUS_INCLUDED_REQUESTS
        overage_cost = overage_requests * COPILOT_PRO_PLUS_OVERAGE_PER_REQUEST
        copilot_total = COPILOT_PRO_PLUS_MONTHLY + overage_cost
        print(f"\n  Copilot Pro+ cost at {total_requests} requests:")
        print(f"    Base:      ${COPILOT_PRO_PLUS_MONTHLY:.2f}")
        print(f"    Overage:   {overage_requests} requests x ${COPILOT_PRO_PLUS_OVERAGE_PER_REQUEST} = ${overage_cost:.2f}")
        print(f"    Total:     ${copilot_total:.2f}")
    else:
        print(f"\n  Note: {total_requests} requests would be within Pro+ included allowance")
        print(f"  (Pro+ includes {COPILOT_PRO_PLUS_INCLUDED_REQUESTS} requests/month)")

    print()


def print_summary_csv(results):
    """Print CSV output of generation costs."""
    print("id,model,input_tokens,output_tokens,total_tokens,cost_usd,created_at")
    for gen in results:
        if gen.get("error"):
            print(f"{gen.get('id', '?')},ERROR,0,0,0,0.0,")
            continue
        gen_id = gen.get("id", "?")
        model = gen.get("model", "?")
        inp = gen.get("tokens_prompt", gen.get("prompt_tokens", 0))
        out = gen.get("tokens_completion", gen.get("completion_tokens", 0))
        cost = extract_cost(gen)
        created = gen.get("created_at", "")
        print(f"{gen_id},{model},{inp},{out},{inp + out},{cost:.6f},{created}")


def print_summary_json(results):
    """Print JSON output of generation costs."""
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "generations": [],
        "summary": {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost_usd": 0.0,
            "generation_count": 0,
        },
    }

    for gen in results:
        if gen.get("error"):
            continue
        inp = gen.get("tokens_prompt", gen.get("prompt_tokens", 0))
        out = gen.get("tokens_completion", gen.get("completion_tokens", 0))
        cost = extract_cost(gen)

        output["generations"].append({
            "id": gen.get("id"),
            "model": gen.get("model"),
            "input_tokens": inp,
            "output_tokens": out,
            "cost_usd": cost,
            "created_at": gen.get("created_at"),
        })

        output["summary"]["total_input_tokens"] += inp
        output["summary"]["total_output_tokens"] += out
        output["summary"]["total_cost_usd"] += cost
        output["summary"]["generation_count"] += 1

    print(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def extract_cost(gen):
    """Extract cost from a generation record, handling multiple field names."""
    cost = gen.get("total_cost")
    if cost is not None:
        return float(cost)
    cost = gen.get("cost")
    if cost is not None:
        return float(cost)
    usage = gen.get("usage")
    if isinstance(usage, dict):
        cost = usage.get("cost")
        if cost is not None:
            return float(cost)
    return 0.0


def format_timestamp(ts):
    """Format a timestamp for display."""
    if not ts:
        return "N/A"
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return str(ts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OpenRouter cost retrieval tool for AI architecture scenario comparison",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # balance
    sub.add_parser("balance", help="Show current API key info and credit balance")

    # generation (single)
    gen_p = sub.add_parser("generation", help="Get cost for a single generation by ID")
    gen_p.add_argument("generation_id", help="The generation ID (e.g., gen-xxxxxxxxxxxxxxxx)")

    # generations (multiple inline)
    gens_p = sub.add_parser("generations", help="Get costs for multiple generation IDs")
    gens_p.add_argument("generation_ids", nargs="+", help="One or more generation IDs")

    # summary (from file)
    summary_p = sub.add_parser("summary", help="Get cost summary from a file of generation IDs")
    summary_p.add_argument("--file", required=True, help="Path to file with generation IDs (one per line)")
    summary_p.add_argument("--format", choices=["text", "csv", "json"], default="text",
                           help="Output format (default: text)")

    args = parser.parse_args()

    commands = {
        "balance": cmd_balance,
        "generation": cmd_generation,
        "generations": cmd_generations,
        "summary": cmd_summary,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
