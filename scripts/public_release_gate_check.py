#!/usr/bin/env python3
"""Repository-local defensive public-release gate scanner.

Standard-library only. No external targets are scanned.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "public-release-gate"
REPORT_JSON = OUT / "public_release_gate_report.json"
REPORT_MD = OUT / "public_release_gate_report.md"
SHA256SUMS = OUT / "SHA256SUMS"

IGNORE_DIR_NAMES = {
    ".git", "node_modules", "vendor", "dist", "build", ".next",
    ".pytest_cache", "__pycache__", ".venv", "venv", ".cache",
}
TEXT_EXTS = {
    "", ".md", ".txt", ".html", ".css", ".js", ".json", ".yml",
    ".yaml", ".toml", ".py", ".sh", ".ps1", ".csv", ".xml", ".svg",
}
BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
    ".gz", ".7z", ".exe", ".dll", ".bin",
}

RULES = (
    ("LOCAL_WINDOWS_USER_PATH", "P1_RELEASE_BLOCKER", re.compile(r"(?i)\b[A-Z]:\\Users\\[^\s`'\"<>]+"), "Potential local Windows user path."),
    ("APPDATA_PATH", "P1_RELEASE_BLOCKER", re.compile(r"(?i)\bAppData\\(?:Roaming|Local|LocalLow)\\[^\s`'\"<>]+"), "Potential AppData path disclosure."),
    ("PRIVATE_EVIDENCE_ROOT", "P1_RELEASE_BLOCKER", re.compile(r"(?i)(cyber-command-console|non[-_ ]public[-_ ]evidence|private[-_ ]evidence[-_ ]root|local[-_ ]evidence[-_ ]root|private-evidence/|local-evidence/)"), "Potential private/local evidence root reference."),
    ("SECRET_ASSIGNMENT", "P1_RELEASE_BLOCKER", re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd|credential)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=:-]{20,}"), "Potential secret-like assignment."),
    ("PRIVATE_KEY_BLOCK", "P1_RELEASE_BLOCKER", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "Private key material marker."),
    ("LOCAL_WINDOWS_TEMP_PATH", "P2_REVIEW_REQUIRED", re.compile(r"(?i)\b[A-Z]:\\(?:Temp|Windows\\Temp)\\[^\s`'\"<>]+"), "Potential local temp path."),
    ("ABSOLUTE_SECURITY_LANGUAGE", "P2_REVIEW_REQUIRED", re.compile(r"(?i)\b(100% secure|fully secure|guaranteed secure|no vulnerabilities|absence of vulnerabilities|completely secure)\b"), "Unsupported absolute security language."),
)

SEVERITY_ORDER = {"P1_RELEASE_BLOCKER": 1, "P2_REVIEW_REQUIRED": 2, "P3_INFORMATIONAL": 3}

ALLOW_MARKERS = (
    "public-release-gate: allow", "allowed example", "prohibited example",
    "example only", "do not use as claim", "pattern definition", "scanner rule", "regex",
)
NEGATION_MARKERS = (
    "does not claim", "do not claim", "not claim", "does not prove", "do not prove",
    "not prove", "no guarantee", "not a guarantee", "not represent", "does not represent",
    "without claiming", "avoid phrasing", "avoid language", "out of scope",
    "proof that vulnerabilities are absent", "that vulnerabilities are absent",
)
PRIVATE_EVIDENCE_REDACTION = re.compile(
    r"(?i)(cyber-command-console|non[-_ ]public[-_ ]evidence|private[-_ ]evidence[-_ ]root|local[-_ ]evidence[-_ ]root|private-evidence/[^\s`'\"<>]*|local-evidence/[^\s`'\"<>]*)"
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ignored_path(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return True
    if path == OUT or OUT in path.parents:
        return True
    return any(part in IGNORE_DIR_NAMES for part in relative.parts)


def binary(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTS:
        return True
    try:
        return b"\x00" in path.read_bytes()[:8192]
    except OSError:
        return True


def files():
    for root, dirs, names in os.walk(ROOT):
        base = Path(root)
        dirs[:] = [d for d in dirs if not ignored_path(base / d)]
        for name in names:
            path = base / name
            if ignored_path(path) or path.suffix.lower() not in TEXT_EXTS or binary(path):
                continue
            yield path


def rule_definition(path: Path, line: str) -> bool:
    if path.name != "public_release_gate_check.py":
        return False
    return any(x in line for x in ("RULES =", "re.compile", "PRIVATE_EVIDENCE_ROOT", "ABSOLUTE_SECURITY_LANGUAGE", "ALLOW_MARKERS", "NEGATION_MARKERS", "PRIVATE_EVIDENCE_REDACTION"))


def allow(path: Path, line: str, rule_id: str) -> bool:
    low = line.lower()
    if any(x in low for x in ALLOW_MARKERS) or rule_definition(path, line):
        return True
    if rule_id == "ABSOLUTE_SECURITY_LANGUAGE" and any(x in low for x in NEGATION_MARKERS):
        return True
    if rule_id == "PRIVATE_EVIDENCE_ROOT" and any(x in low for x in ("out of scope", "not committed", "not sanitized", "move ")):
        return True
    return False


def clean(line: str) -> str:
    s = line.strip().replace("\t", " ")
    s = re.sub(r"(?i)(api[_-]?key|token|secret|password|passwd|credential)\s*[:=]\s*['\"]?[^\s'\"]+", r"\1=<REDACTED>", s)
    s = re.sub(r"(?i)[A-Z]:\\Users\\[^\s`'\"<>]+", "<LOCAL_USER_PATH_REDACTED>", s)
    s = re.sub(r"(?i)AppData\\(?:Roaming|Local|LocalLow)\\[^\s`'\"<>]+", "<APPDATA_PATH_REDACTED>", s)
    s = PRIVATE_EVIDENCE_REDACTION.sub("<PRIVATE_OR_LOCAL_EVIDENCE_REDACTED>", s)
    return s[:157] + "..." if len(s) > 160 else s


def scan(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for rule_id, sev, pattern, desc in RULES:
            if allow(path, line, rule_id):
                continue
            if pattern.search(line):
                out.append({
                    "file": rel(path), "line": n, "rule_id": rule_id,
                    "severity": sev, "description": desc, "snippet": clean(line),
                })
    return out


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write(files_scanned: int, findings: list[dict]) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    counts = {sev: sum(1 for f in findings if f["severity"] == sev) for sev in SEVERITY_ORDER}
    ordered = sorted(findings, key=lambda f: (SEVERITY_ORDER[f["severity"]], f["file"], f["line"]))
    report = {
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "scope": "repository-local defensive public-release validation only",
        "files_scanned": files_scanned,
        "findings_total": len(findings),
        "p1_release_blockers": counts["P1_RELEASE_BLOCKER"],
        "p2_review_required": counts["P2_REVIEW_REQUIRED"],
        "p3_informational": counts["P3_INFORMATIONAL"],
        "findings": ordered,
        "limitations": [
            "Static pattern review only; not an external audit.",
            "No external targets were scanned.",
            "No guarantee that vulnerabilities are absent.",
            "Binary/PDF/image files are skipped unless they are valid text.",
        ],
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md = [
        "# Public Release Gate Report", "",
        f"Generated UTC: `{report['generated_at_utc']}`", "",
        "## Scope", "", "Repository-local defensive public-release validation only. No external targets were scanned.", "",
        "## Summary", "",
        f"- Files scanned: `{files_scanned}`",
        f"- Findings total: `{len(findings)}`",
        f"- P1 release blockers: `{counts['P1_RELEASE_BLOCKER']}`",
        f"- P2 review required: `{counts['P2_REVIEW_REQUIRED']}`",
        f"- P3 informational: `{counts['P3_INFORMATIONAL']}`", "", "## Findings", "",
    ]
    if not ordered:
        md.append("No findings were detected by this static scanner.")
    for f in ordered:
        md += [
            f"### {f['severity']} — {f['rule_id']}", "",
            f"- File: `{f['file']}`", f"- Line: `{f['line']}`",
            f"- Description: {f['description']}", f"- Sanitized snippet: `{f['snippet']}`", "",
        ]
    md += ["", "## Limitations", "", "- This is static release-gate evidence, not a certification or external audit.", "- The scanner does not prove that vulnerabilities are absent.", "- Reviewers must correlate findings with README claims, evidence manifest, residual risk, and project issues.", ""]
    REPORT_MD.write_text("\n".join(md), encoding="utf-8")
    SHA256SUMS.write_text("".join(f"{sha(p)}  {rel(p)}\n" for p in (REPORT_JSON, REPORT_MD)), encoding="utf-8")
    return report


def main() -> int:
    findings = []
    count = 0
    for path in files():
        count += 1
        findings.extend(scan(path))
    report = write(count, findings)
    summary = {k: report[k] for k in ("files_scanned", "findings_total", "p1_release_blockers", "p2_review_required", "p3_informational")}
    print(json.dumps(summary, sort_keys=True))
    return 1 if report["p1_release_blockers"] else 0


if __name__ == "__main__":
    sys.exit(main())
