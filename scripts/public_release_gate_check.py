#!/usr/bin/env python3
"""Repository-local public release gate scanner.

Defensive validation only. The scanner inspects the current repository tree for
public-release risks such as local/private path disclosure, secret-like strings,
and unsupported absolute security language. It does not scan external targets and
uses only the Python standard library.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "evidence" / "public-release-gate"
REPORT_JSON = OUT_DIR / "public_release_gate_report.json"
REPORT_MD = OUT_DIR / "public_release_gate_report.md"
SHA_FILE = OUT_DIR / "SHA256SUMS"

IGNORE_DIRS = {
    ".git",
    ".github/.cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".next",
    ".venv",
    "venv",
}

TEXT_EXTENSIONS = {
    "",
    ".md",
    ".txt",
    ".html",
    ".css",
    ".js",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".py",
    ".sh",
    ".ps1",
    ".csv",
    ".xml",
    ".svg",
}

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".7z",
    ".exe",
    ".dll",
    ".bin",
}

RULES: Tuple[Dict[str, object], ...] = (
    {
        "id": "LOCAL_WINDOWS_USER_PATH",
        "severity": "P1_RELEASE_BLOCKER",
        "pattern": re.compile(r"(?i)\b[A-Z]:\\\\Users\\\\[^\s`'\"<>]+"),
        "description": "Potential local Windows user path in public content.",
    },
    {
        "id": "LOCAL_WINDOWS_TEMP_PATH",
        "severity": "P2_REVIEW_REQUIRED",
        "pattern": re.compile(r"(?i)\b[A-Z]:\\\\(?:Temp|Windows\\\\Temp)\\\\[^\s`'\"<>]+"),
        "description": "Potential local temp path in public content.",
    },
    {
        "id": "APPDATA_PATH",
        "severity": "P1_RELEASE_BLOCKER",
        "pattern": re.compile(r"(?i)\bAppData\\\\(?:Roaming|Local|LocalLow)\\\\[^\s`'\"<>]+"),
        "description": "Potential AppData path disclosure.",
    },
    {
        "id": "PRIVATE_EVIDENCE_ROOT",
        "severity": "P1_RELEASE_BLOCKER",
        "pattern": re.compile(r"(?i)(private[-_ ]evidence|local[-_ ]evidence|cyber-command-console|non[-_ ]public[-_ ]evidence)"),
        "description": "Potential private/local evidence reference.",
    },
    {
        "id": "SECRET_ASSIGNMENT",
        "severity": "P1_RELEASE_BLOCKER",
        "pattern": re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd|credential)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=:-]{20,}"),
        "description": "Potential secret-like assignment.",
    },
    {
        "id": "PRIVATE_KEY_BLOCK",
        "severity": "P1_RELEASE_BLOCKER",
        "pattern": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
        "description": "Private key material marker.",
    },
    {
        "id": "ABSOLUTE_SECURITY_LANGUAGE",
        "severity": "P2_REVIEW_REQUIRED",
        "pattern": re.compile(r"(?i)\b(100% secure|fully secure|guaranteed secure|no vulnerabilities|absence of vulnerabilities|completely secure)\b"),
        "description": "Unsupported absolute security language.",
    },
)

ALLOWLIST_MARKERS = (
    "public-release-gate: allow",
    "allowed example",
    "prohibited example",
    "example only",
    "do not use as claim",
    "pattern definition",
    "scanner rule",
    "regex",
)

SEVERITY_ORDER = {
    "P1_RELEASE_BLOCKER": 1,
    "P2_REVIEW_REQUIRED": 2,
    "P3_INFORMATIONAL": 3,
}


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def should_ignore_dir(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix() if path != ROOT else ""
    return rel in IGNORE_DIRS or any(rel.startswith(d + "/") for d in IGNORE_DIRS)


def is_probably_binary(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    try:
        sample = path.read_bytes()[:8192]
    except OSError:
        return True
    return b"\x00" in sample


def iter_candidate_files() -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        current = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not should_ignore_dir(current / d)]
        for filename in filenames:
            path = current / filename
            if should_ignore_dir(path.parent):
                continue
            if path.suffix.lower() in BINARY_EXTENSIONS:
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if is_probably_binary(path):
                continue
            yield path


def is_allowlisted(line: str) -> bool:
    lower = line.lower()
    return any(marker in lower for marker in ALLOWLIST_MARKERS)


def sanitize_snippet(line: str) -> str:
    cleaned = line.strip().replace("\t", " ")
    cleaned = re.sub(r"(?i)(api[_-]?key|token|secret|password|passwd|credential)\s*[:=]\s*['\"]?[^\s'\"]+", r"\1=<REDACTED>", cleaned)
    cleaned = re.sub(r"(?i)[A-Z]:\\\\Users\\\\[^\s`'\"<>]+", r"<LOCAL_USER_PATH_REDACTED>", cleaned)
    cleaned = re.sub(r"(?i)AppData\\\\(?:Roaming|Local|LocalLow)\\\\[^\s`'\"<>]+", r"<APPDATA_PATH_REDACTED>", cleaned)
    if len(cleaned) > 160:
        return cleaned[:157] + "..."
    return cleaned


def scan_file(path: Path) -> List[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return findings
    except OSError:
        return findings

    rel = path.relative_to(ROOT).as_posix()
    for line_no, line in enumerate(text.splitlines(), start=1):
        if is_allowlisted(line):
            continue
        for rule in RULES:
            pattern = rule["pattern"]
            assert isinstance(pattern, re.Pattern)
            if pattern.search(line):
                findings.append(
                    {
                        "file": rel,
                        "line": line_no,
                        "rule_id": rule["id"],
                        "severity": rule["severity"],
                        "description": rule["description"],
                        "snippet": sanitize_snippet(line),
                    }
                )
    return findings


def count_by_severity(findings: List[Dict[str, object]]) -> Dict[str, int]:
    return {
        severity: sum(1 for f in findings if f.get("severity") == severity)
        for severity in SEVERITY_ORDER
    }


def write_reports(files_scanned: int, findings: List[Dict[str, object]]) -> Dict[str, object]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    counts = count_by_severity(findings)
    report = {
        "generated_at_utc": utc_now(),
        "scope": "repository-local defensive public-release validation only",
        "files_scanned": files_scanned,
        "findings_total": len(findings),
        "p1_release_blockers": counts["P1_RELEASE_BLOCKER"],
        "p2_review_required": counts["P2_REVIEW_REQUIRED"],
        "p3_informational": counts["P3_INFORMATIONAL"],
        "findings": sorted(findings, key=lambda f: (SEVERITY_ORDER[str(f["severity"])], str(f["file"]), int(f["line"]))),
        "limitations": [
            "Static pattern review only; not an external audit.",
            "No external targets were scanned.",
            "No guarantee of absence of vulnerabilities.",
            "Binary/PDF/image files are skipped unless they are valid text.",
        ],
    }

    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Public Release Gate Report",
        "",
        f"Generated UTC: `{report['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "Repository-local defensive public-release validation only. No external targets were scanned.",
        "",
        "## Summary",
        "",
        f"- Files scanned: `{files_scanned}`",
        f"- Findings total: `{len(findings)}`",
        f"- P1 release blockers: `{counts['P1_RELEASE_BLOCKER']}`",
        f"- P2 review required: `{counts['P2_REVIEW_REQUIRED']}`",
        f"- P3 informational: `{counts['P3_INFORMATIONAL']}`",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No findings were detected by this static scanner.")
    else:
        for f in report["findings"]:
            lines.extend(
                [
                    f"### {f['severity']} — {f['rule_id']}",
                    "",
                    f"- File: `{f['file']}`",
                    f"- Line: `{f['line']}`",
                    f"- Description: {f['description']}",
                    f"- Sanitized snippet: `{f['snippet']}`",
                    "",
                ]
            )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This is static release-gate evidence, not a certification or external audit.",
            "- The scanner does not prove absence of vulnerabilities.",
            "- Reviewers must correlate findings with README claims, evidence manifest, residual risk, and project issues.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    generated = [REPORT_JSON, REPORT_MD]
    SHA_FILE.write_text(
        "".join(f"{sha256_file(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in generated),
        encoding="utf-8",
    )
    return report


def main() -> int:
    findings: List[Dict[str, object]] = []
    files_scanned = 0
    for path in iter_candidate_files():
        files_scanned += 1
        findings.extend(scan_file(path))

    report = write_reports(files_scanned, findings)
    print(json.dumps({k: report[k] for k in ("files_scanned", "findings_total", "p1_release_blockers", "p2_review_required", "p3_informational")}, sort_keys=True))
    return 1 if report["p1_release_blockers"] else 0


if __name__ == "__main__":
    sys.exit(main())
