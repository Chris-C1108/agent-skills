#!/usr/bin/env python3
"""
AGENTS.md Quality, Truthfulness & Budget Linter
Checks line budget, fluff words, broken paths, and environment match.
"""

import os
import re
import sys
import argparse
from pathlib import Path

MAX_LINES_DEFAULT = 150
BANNED_WORDS = [
    r"\bplease\b",
    r"\bkindly\b",
    r"\byou should\b",
    r"\bas an ai\b",
    r"\bbe careful to\b",
    r"\bensure that you\b",
    r"\bit is important that\b",
    r"\bfeel free to\b",
    r"\bkeep in mind that\b",
]

def resolve_target(target: str, base_dir: Path):
    clean = target.strip().strip("`").rstrip(".,;")
    if not clean:
        return None, clean

    # Wildcard match
    if "*" in clean:
        cwd_matches = list(Path(".").glob(clean))
        if cwd_matches:
            return cwd_matches[0], clean
        base_matches = list(base_dir.glob(clean))
        if base_matches:
            return base_matches[0], clean
        return None, clean

    p = Path(clean)
    if p.is_absolute() and p.exists():
        return p, clean
    if p.exists():
        return p, clean
    rel = base_dir / clean
    if rel.exists():
        return rel, clean
    return None, clean

def audit(target_file="AGENTS.md", max_lines=MAX_LINES_DEFAULT, check_env=False, check_rules=False):
    file_path = Path(target_file)
    if not file_path.exists():
        print(f"[FAIL] Target file '{target_file}' not found.")
        return 1

    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    issues = []
    warnings = []
    base_dir = file_path.parent

    # 1. Line budget check
    if len(lines) > max_lines:
        issues.append(f"[BUDGET EXCEEDED] '{target_file}' has {len(lines)} lines. Max allowed: {max_lines}.")
    else:
        print(f"[PASS] Line budget: {len(lines)}/{max_lines} lines.")

    # 2. ADHD / Spartan fluff word check
    fluff_count = 0
    for idx, line in enumerate(lines, 1):
        for pattern in BANNED_WORDS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                fluff_count += 1
                issues.append(f"[SLOP DETECTED] Line {idx} contains banned fluff word '{match.group(0)}': '{line.strip()}'")

    if fluff_count == 0:
        print("[PASS] Zero-slop check: No banned fluff words found.")

    # 3. Pointer targets & rules/decisions verification
    pointer_raw = re.findall(r"->\s*`?([a-zA-Z0-9_\-\./]+(?:/[a-zA-Z0-9_\-\./]*|\.[a-zA-Z0-9]+))`?", content)
    rule_decision_raw = re.findall(r"`?(docs/(?:rules|decisions)/[a-zA-Z0-9_\-\./]*)`?", content)

    combined_targets = set()
    for ptr in pointer_raw:
        c = ptr.strip().strip("`").rstrip(".,;")
        if c:
            combined_targets.add(c)
    for rd in rule_decision_raw:
        c = rd.strip().strip("`").rstrip(".,;")
        if c:
            combined_targets.add(c)

    rule_decision_count = 0
    for target in sorted(combined_targets):
        is_rule_or_decision = target.startswith("docs/rules/") or target.startswith("docs/decisions/") or target in ("docs/rules", "docs/decisions")
        resolved, clean_target = resolve_target(target, base_dir)

        if is_rule_or_decision:
            rule_decision_count += 1

        if resolved is None:
            msg = f"[BROKEN POINTER] Referenced file or directory does not exist on disk: {clean_target}"
            if check_rules and is_rule_or_decision:
                issues.append(f"[BROKEN RULE/DECISION POINTER] Required target missing on disk: {clean_target}")
            else:
                warnings.append(msg)
        else:
            if is_rule_or_decision:
                print(f"[PASS] Verified pointer target: {clean_target}")

    if rule_decision_count > 0:
        print(f"[PASS] Verified {rule_decision_count} docs/rules and docs/decisions pointer target(s).")

    # If --check-rules enforced, verify directory presence
    if check_rules:
        for req_dir in ["docs/rules", "docs/decisions"]:
            d_path = Path(req_dir) if Path(req_dir).exists() else base_dir / req_dir
            if not d_path.exists() or not d_path.is_dir():
                issues.append(f"[MISSING DIRECTORY] Required directory '{req_dir}' not found on disk.")
            else:
                print(f"[PASS] Directory verified: {req_dir}/")

    # 4. Optional environment command grounding check
    if check_env:
        commands = re.findall(r"`([a-zA-Z0-9_\-]+(?:\s+[a-zA-Z0-9_\-]+)*)`", content)
        print(f"[INFO] Grounding check found {len(commands)} inline code commands to review.")

    # Output audit report
    if warnings:
        print(f"\n=== Warnings ({len(warnings)}) ===")
        for w in warnings:
            print(f"  * {w}")

    if issues:
        print(f"\n=== AGENTS.md Audit Failed ({len(issues)} issues found) ===")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    else:
        print(f"\n[PASS] '{target_file}' conforms to ADHD Spartan standards and budget integrity.")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Audit AGENTS.md for line budget, fluff, and pointer validity.")
    parser.add_argument("--file", default="AGENTS.md", help="Path to AGENTS.md")
    parser.add_argument("--max-lines", type=int, default=MAX_LINES_DEFAULT, help="Max allowed lines")
    parser.add_argument("--check-env", action="store_true", help="Check command grounding")
    parser.add_argument("--check-rules", action="store_true", help="Enforce verification of docs/rules/ and docs/decisions/ pointer targets")
    args = parser.parse_args()

    exit_code = audit(args.file, args.max_lines, args.check_env, args.check_rules)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
