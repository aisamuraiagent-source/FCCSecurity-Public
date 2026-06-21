# Local Validation

## Status

This document records executed validation for the public static preview after PR #5 defensive governance remediation.

## Executed commands and checks

```powershell
# Required governance artifacts
Test-Path for SECURITY.md and canonical docs/* governance artifacts

# Root/docs mirror integrity
Get-FileHash -Algorithm SHA256 for root governance mirrors and docs/ copies

# Runtime unchanged in this remediation
git diff --exit-code -- app.js index.html styles.css

# JavaScript syntax
node --check app.js

# Runtime sink search
rg -n "innerHTML|outerHTML|insertAdjacentHTML|eval\(|new Function|document.write" app.js index.html styles.css

# High-confidence secret/key scan
rg -n $secretPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'

# Suspicious assignment scan
rg -n $assignmentPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'

# Private path and credential-bearing URL hygiene
rg -n $privatePathPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/security-scans/**' --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'

# Deprecated raw remote command check
Search the repository for the deprecated raw verbose remote command string and require no matches.

# Whitespace/diff hygiene
git diff --check
```

## Browser validation

A local loopback preview was served with:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Chrome Browser Use validated `http://127.0.0.1:4173/` with these observed results:

- title: `FCC Security - Frontier Cyber Intelligence`;
- H1: `Risk, evidence, validation, action.`;
- present IDs: `signalList`, `threatList`, `ledgerRows`, `timelineList`, `detailTitle`, `riskScore`, `exportSnapshot`;
- counts: 3 nav items, 4 filters, 6 panels, 5 signal items, 4 threat items, 4 ledger rows, 6 timeline items;
- active filter: `all`;
- console errors: none.

A prior direct `file:///C:/tmp/.../index.html` browser attempt was blocked by Browser Use URL policy; no workaround was attempted. Loopback validation is the executed browser evidence.

## Expected result

- No private paths or high-confidence secret-like tokens in active public files.
- No dangerous dynamic code execution sinks in runtime files.
- JavaScript syntax check passes.
- Whitespace check passes.
- Local preview binds only to `127.0.0.1`.
- Browser render smoke check passes without console errors.

## Current limitation

No CI workflow was added or executed in this remediation. GitHub review comments were not replied to or resolved through the GitHub UI.
