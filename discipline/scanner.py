"""Discipline scanner — R1/R2/R3 enforcement for piratetok_live."""

import os
import re
import sys

MAX_LOC = 800
SRC_DIR = "piratetok_live"
violations = 0


def check_file(path: str) -> None:
    global violations
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    rel = os.path.relpath(path)

    # R1: LOC limit
    if len(lines) > MAX_LOC:
        print(f"R1 {rel} — {len(lines)} lines (max {MAX_LOC})", file=sys.stderr)
        violations += 1

    for i, raw_line in enumerate(lines, 1):
        line = raw_line.strip()

        # R2: bare except
        if line == "except:":
            print(f"R2 {rel}:{i} — bare except", file=sys.stderr)
            violations += 1
        if re.search(r"except\s+Exception\s*:\s*$", line):
            print(f"R2 {rel}:{i} — bare except Exception", file=sys.stderr)
            violations += 1
        if "except Exception: pass" in line or "except: pass" in line:
            print(f"R2 {rel}:{i} — swallowed exception: {line}", file=sys.stderr)
            violations += 1

        # R3: glob imports
        if re.search(r"from\s+\S+\s+import\s+\*", line):
            print(f"R3 {rel}:{i} — glob import: {line}", file=sys.stderr)
            violations += 1


def walk(directory: str) -> None:
    for root, _dirs, files in os.walk(directory):
        for name in files:
            if not name.endswith(".py"):
                continue
            check_file(os.path.join(root, name))


walk(SRC_DIR)

if violations > 0:
    print(f"\n{violations} discipline violation(s) found", file=sys.stderr)
    sys.exit(1)
print("discipline check passed")
