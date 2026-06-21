# Remediation Backlog

## Immediate

| ID | Priority | Status | Action | Owner gate |
| --- | --- | --- | --- | --- |
| RB-001 | High | Done | Add `AGENTS.md` with repo-scoped defensive governance. | Human review before future edits. |
| RB-002 | High | Done | Add security scope, policy, test plan, findings ledger, runtime guardrails, and audit evidence docs. | Human review. |
| RB-003 | Medium | Done | Materialize README-referenced validation/threat-model evidence paths. | Human review. |
| RB-007 | Medium | Done | Add canonical `docs/` governance packet and keep root mirrors for PR compatibility. | Required artifact path check. |
| RB-008 | Medium | Done | Clarify that repository secret exposure is in scope while raw secret values must not be repeated. | Manual policy review. |
| RB-009 | Medium | Done | Remove raw raw verbose remote listing from allowlisted evidence commands. | Search for the deprecated raw remote command string. |
| RB-010 | Medium | Done | Replace noisy secret scan with high-confidence token/key checks plus separate private-path hygiene check. | Review `SAFETY_TEST_PLAN.md`. |
| RB-011 | Medium | Done | Keep README references limited to committed `docs/` artifacts. | Link/path existence check. |

## Next approved patch

| ID | Priority | Status | Action | Validation |
| --- | --- | --- | --- | --- |
| RB-004 | Medium | Proposed | Add a static security check workflow only after explicit CI/CD approval. | Check for private paths, token patterns, dangerous JS sinks, and syntax errors. |
| RB-005 | Low | Proposed | Review UI copy for warnings against entering real secrets/logs. | Manual review and screenshot/DOM check. |
| RB-006 | Low | Done | Add a short README link section to the new security docs. | README link check. |
