# Safety Test Plan

## Objective

Validate that the public static preview remains defensive, local-first, and free of avoidable public security risks.

## Checks

1. Repository scope
   - Confirm public files match `SECURITY_SCOPE.md`.
   - Confirm no private paths, hostnames, account emails, raw secret values, or raw logs appear in public docs.
   - Confirm repository-scoped secret exposure reports remain accepted without repeating raw secret values.

2. Static app behavior
   - Review `index.html` for external scripts, unsafe inline handlers, and missing defensive headers where applicable.
   - Review `app.js` for dangerous sinks, dynamic execution, unsafe HTML insertion, storage of sensitive data, and export behavior.
   - Review `styles.css` for external imports or remote resources.

3. Documentation consistency
   - Confirm README links and referenced evidence files exist in the current repository tree.
   - Confirm public disclaimers do not overclaim affiliation, certification, or production readiness.

4. Runtime guardrails
   - Confirm `docs/RUNTIME_GUARDRAILS.yaml`, `docs/APPROVAL_GATES.md`, `docs/SAFE_COMMAND_ALLOWLIST.md`, `docs/DENYLISTED_ACTIONS.md`, `docs/MONITORING_RULES.md`, and `docs/ENFORCEMENT_DECISIONS.md` exist.
   - Confirm root-level mirrors exist only for GitHub/PR compatibility and match the canonical `docs/` artifacts.

## Proposed validation commands

Do not execute without approval:

```powershell
$required = @(
  "SECURITY.md",
  "docs/SECURITY.md",
  "docs/SECURITY_SCOPE.md",
  "docs/SECURITY_POLICY.md",
  "docs/ALLOWED_DISALLOWED_ACTIONS.md",
  "docs/TOOL_PERMISSION_MATRIX.md",
  "docs/SAFETY_TEST_PLAN.md",
  "docs/SECURITY_FINDINGS.md",
  "docs/ADVERSARIAL_REVIEW_NOTES.md",
  "docs/REMEDIATION_BACKLOG.md",
  "docs/RUNTIME_GUARDRAILS.yaml",
  "docs/APPROVAL_GATES.md",
  "docs/SAFE_COMMAND_ALLOWLIST.md",
  "docs/DENYLISTED_ACTIONS.md",
  "docs/MONITORING_RULES.md",
  "docs/INCIDENT_LOG.csv",
  "docs/INVESTIGATION_TEMPLATE.md",
  "docs/EVIDENCE_LOG.md",
  "docs/ENFORCEMENT_DECISIONS.md",
  "docs/CORRECTIVE_ACTIONS.md",
  "docs/PATCH_VALIDATION_REPORT.md",
  "docs/AUDIT_EVIDENCE_PACK.md"
)
$missing = $required | Where-Object { -not (Test-Path -LiteralPath $_) }
if ($missing) { $missing; exit 1 }

$secretPattern = 'ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9][A-Za-z0-9_-]{18,}|-----BEGIN (RSA |OPENSSH |EC |DSA |)?PRIVATE KEY-----'
rg -n $secretPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'

$assignmentPattern = '(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[''"]?[A-Za-z0-9_./+=-]{20,}'
rg -n $assignmentPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'

$privatePathPattern = 'C:' + '\\Users\\|file:///C:/Users|://[^/@\s]+@'
rg -n $privatePathPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/security-scans/**' --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'

rg -n "innerHTML|outerHTML|insertAdjacentHTML|eval\(|new Function|document.write" app.js index.html styles.css
node --check app.js
git diff --check
```
