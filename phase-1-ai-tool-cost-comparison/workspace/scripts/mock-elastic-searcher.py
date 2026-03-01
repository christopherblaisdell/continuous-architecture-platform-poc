#!/usr/bin/env python3
"""Mock Elasticsearch Searcher - Simulates production log queries for NovaTrek Architecture Practice.

This script provides a synthetic Elasticsearch query interface that loads log
entries from a local JSON file. Includes a ProductionElasticSearcher class
that mirrors the real tool's interface. Used for testing AI coding assistants.

Usage:
    # Search all logs
    python mock-elastic-searcher.py

    # Filter by service
    python mock-elastic-searcher.py --service svc-scheduling-orchestrator

    # Filter by log level
    python mock-elastic-searcher.py --level ERROR

    # Filter by time range (last N hours)
    python mock-elastic-searcher.py --hours 24

    # Free-text search
    python mock-elastic-searcher.py --query "overwritten"

    # Combined filters
    python mock-elastic-searcher.py --service svc-check-in --level ERROR --hours 48

Requires: Python 3.10+ (stdlib only, no external dependencies)
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# Resolve mock data path relative to this script
MOCK_DATA_DIR = Path(__file__).parent / "mock-data"
LOGS_FILE = MOCK_DATA_DIR / "elastic-logs.json"

# ANSI color codes for terminal output
COLORS = {
    "ERROR": "\033[91m",  # Red
    "WARN": "\033[93m",   # Yellow
    "INFO": "\033[92m",   # Green
    "DEBUG": "\033[90m",  # Gray
    "RESET": "\033[0m",
}


class ProductionElasticSearcher:
    """Simulates the production Elasticsearch searcher interface.

    This class mirrors the real ProductionElasticSearcher used in the NovaTrek
    Architecture Practice tooling, providing a search() method with identical
    parameter semantics.
    """

    def __init__(self, data_file: Optional[Path] = None):
        """Initialize the searcher with a path to the mock log data file.

        Args:
            data_file: Path to the JSON file containing mock log entries.
                       Defaults to mock-data/elastic-logs.json.
        """
        self.data_file = data_file or LOGS_FILE
        self._logs = self._load_logs()

    def _load_logs(self) -> list:
        """Load log entries from the mock-data JSON file."""
        if not self.data_file.exists():
            print(f"ERROR: Mock data file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def search(
        self,
        service: Optional[str] = None,
        level: Optional[str] = None,
        hours: Optional[int] = None,
        query: Optional[str] = None,
    ) -> list:
        """Search log entries with optional filters.

        Args:
            service: Filter by service name (case-insensitive partial match).
            level: Filter by log level (ERROR, WARN, INFO, DEBUG).
            hours: Only include entries from the last N hours.
            query: Free-text search across message field.

        Returns:
            List of matching log entry dicts.
        """
        results = list(self._logs)

        # Filter by service name (partial, case-insensitive)
        if service:
            service_lower = service.lower()
            results = [e for e in results if service_lower in e.get("service", "").lower()]

        # Filter by log level (exact, case-insensitive)
        if level:
            level_upper = level.upper()
            results = [e for e in results if e.get("level", "").upper() == level_upper]

        # Filter by time range
        if hours:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
            filtered = []
            for entry in results:
                try:
                    ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                    if ts >= cutoff:
                        filtered.append(entry)
                except (ValueError, KeyError):
                    # Include entries with unparseable timestamps
                    filtered.append(entry)
            results = filtered

        # Free-text search in message field
        if query:
            query_lower = query.lower()
            results = [e for e in results if query_lower in e.get("message", "").lower()]

        return results


def format_log_entry(entry: dict, use_color: bool = True) -> str:
    """Format a single log entry for terminal output."""
    level = entry.get("level", "???")
    color = COLORS.get(level, "") if use_color else ""
    reset = COLORS["RESET"] if use_color else ""

    timestamp = entry.get("timestamp", "N/A")
    service = entry.get("service", "unknown")
    message = entry.get("message", "")
    trace_id = entry.get("traceId", "")
    request_path = entry.get("requestPath", "")

    line = f"  {color}[{level:5s}]{reset} {timestamp}  {service:36s} {message}"
    if trace_id:
        line += f"\n         traceId={trace_id}"
    if request_path:
        line += f"  path={request_path}"
    return line


def print_log_results(entries: list) -> None:
    """Print formatted log search results."""
    border = "-" * 120
    print(f"\n  Elasticsearch Results ({len(entries)} entries)")
    print(border)
    for entry in entries:
        print(format_log_entry(entry))
    print(border)
    print()


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with help text."""
    parser = argparse.ArgumentParser(
        prog="mock-elastic-searcher.py",
        description="Mock Elasticsearch Searcher - Query synthetic production logs.",
        epilog="Examples:\n"
               "  python mock-elastic-searcher.py --service svc-scheduling-orchestrator\n"
               "  python mock-elastic-searcher.py --level ERROR\n"
               "  python mock-elastic-searcher.py --query 'overwritten' --level ERROR\n"
               "  python mock-elastic-searcher.py --service svc-check-in --hours 48",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--service", metavar="NAME", help="Filter by service name (partial match)")
    parser.add_argument("--level", metavar="LEVEL", choices=["ERROR", "WARN", "INFO", "DEBUG"],
                        help="Filter by log level")
    parser.add_argument("--hours", metavar="N", type=int, help="Only show entries from the last N hours")
    parser.add_argument("--query", metavar="TEXT", help="Free-text search in log messages")
    return parser


def main() -> None:
    """Entry point for the mock Elasticsearch searcher."""
    parser = build_parser()
    args = parser.parse_args()

    searcher = ProductionElasticSearcher()
    results = searcher.search(
        service=args.service,
        level=args.level,
        hours=args.hours,
        query=args.query,
    )
    print_log_results(results)


if __name__ == "__main__":
    main()
