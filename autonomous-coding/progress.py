"""
Progress Tracking Utilities
===========================

Functions for tracking and displaying progress of the autonomous coding agent.
"""

import json
from pathlib import Path

PROGRESS_BAR_WIDTH = 40


def count_passing_tests(project_dir: Path) -> tuple[int, int]:
    """
    Count passing and total tests in feature_list.json.

    Args:
        project_dir: Directory containing feature_list.json

    Returns:
        (passing_count, total_count)
    """
    tests_file = project_dir / "feature_list.json"

    if not tests_file.exists():
        return 0, 0

    try:
        with open(tests_file, "r", encoding="utf-8") as f:
            tests = json.load(f)
    except (json.JSONDecodeError, IOError):
        return 0, 0

    # The agent edits this file directly, so don't assume it kept the shape
    if not isinstance(tests, list):
        return 0, 0

    total = len(tests)
    passing = sum(
        1 for test in tests if isinstance(test, dict) and test.get("passes", False)
    )

    return passing, total


def format_progress_bar(passing: int, total: int, width: int = PROGRESS_BAR_WIDTH) -> str:
    """Render a fixed-width text progress bar, e.g. [#####-----]."""
    filled = int(width * passing / total) if total > 0 else 0
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def print_session_header(session_num: int, is_initializer: bool) -> None:
    """Print a formatted header for the session."""
    session_type = "INITIALIZER" if is_initializer else "CODING AGENT"

    print("\n" + "=" * 70)
    print(f"  SESSION {session_num}: {session_type}")
    print("=" * 70)
    print()


def print_progress_summary(project_dir: Path) -> None:
    """Print a summary of current progress."""
    passing, total = count_passing_tests(project_dir)

    if total > 0:
        percentage = (passing / total) * 100
        print(f"\nProgress: {passing}/{total} tests passing ({percentage:.1f}%)")
        print(f"          {format_progress_bar(passing, total)}")
    elif (project_dir / "feature_list.json").exists():
        print(
            "\nProgress: feature_list.json exists but could not be read "
            "(empty, invalid JSON, or not a list of tests)"
        )
    else:
        print("\nProgress: feature_list.json not yet created")
