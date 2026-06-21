# Remediation Backlog

## Immediate

| ID | Priority | Status | Action | Owner gate |
| --- | --- | --- | --- | --- |
| RB-001 | High | Done | Add `AGENTS.md` with repo-scoped defensive governance. | Human review before future edits. |
| RB-002 | High | Done | Add security scope, policy, test plan, findings ledger, runtime guardrails, and audit evidence docs. | Human review. |
| RB-003 | Medium | Done | Materialize README-referenced validation/threat-model evidence paths. | Human review. |

## Next approved patch

| ID | Priority | Status | Action | Validation |
| --- | --- | --- | --- | --- |
| RB-004 | Medium | Proposed | Add a static security check workflow only after explicit CI/CD approval. | Check for private paths, token patterns, dangerous JS sinks, and syntax errors. |
| RB-005 | Low | Proposed | Review UI copy for warnings against entering real secrets/logs. | Manual review and screenshot/DOM check. |
| RB-006 | Low | Proposed | Add a short README link section to the new security docs. | README link check. |
