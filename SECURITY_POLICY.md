# Security Policy

## Central rule

Only perform defensive review, correction, validation, and documentation inside the authorized repository scope.

## Required controls

- Prefer static analysis before execution.
- Do not access network resources without explicit human approval.
- Do not modify files without explicit human approval.
- Do not print or store secrets.
- Do not include private local paths, hostnames, IPs, account emails, tokens, keys, or raw logs in public evidence.
- Treat `HIGH` and `CRITICAL` findings as release blockers.
- Keep decisions traceable to observable evidence.

## Public wording control

Do not imply affiliation, endorsement, sponsorship, certification, or partnership with OpenAI, Codex, Codex Security, DayBreak, or any third-party platform. Tool references must be factual and limited to workflow context.

## Validation rule

A security correction is not complete until the expected behavior, validation command or manual check, observed result, residual risk, and evidence location are documented.
