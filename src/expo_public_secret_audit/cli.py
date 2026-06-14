from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .scanner import scan_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan Expo env/config files for risky public secrets."
    )
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()

    findings = []
    for path in args.files:
        findings.extend(scan_text(path.read_text(), source=str(path)))

    for finding in findings:
        print(f"{finding.source}:{finding.line}: {finding.name} -> {finding.reason}")

    if findings:
        sys.exit(1)
