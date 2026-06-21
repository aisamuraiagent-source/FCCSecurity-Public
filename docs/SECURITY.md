# Security Policy

## Supported scope

This repository is a public sanitized static preview for `FCCSecurity-Public`.
The supported security scope is limited to the static files and documentation in this repository:

- `.nojekyll`
- `README.md`
- `AGENTS.md`
- `index.html`
- `styles.css`
- `app.js`
- security documentation and sanitized evidence committed to this repository

Repository-scoped secret exposure is in scope when the report identifies that this public repository may contain a committed token, key, credential, or secret-like value. Reports must describe the location and risk without including raw secret values.

Out of scope: third-party public targets, private repositories, raw credential/token/key values, live logs, production systems, network scanning, exploitation, persistence, evasion, malware, credential collection, and destructive actions.

## Reporting guidance

Report only defensive, repository-scoped issues. Do not include secrets, local machine paths, private hostnames, private IPs, screenshots with sensitive data, raw logs, account email, tokens, keys, or internal IDs.

## Handling rules

- `LOW`: document and monitor.
- `MEDIUM`: fix or explicitly accept risk.
- `HIGH`: block merge/release until fixed and validated.
- `CRITICAL`: suspend affected flow, require formal human review, fix, validate, and document.

## Public disclaimer

References to Codex, Codex Security, OpenAI, or DayBreak describe tooling or workflow context only. They do not claim affiliation, endorsement, certification, sponsorship, or partnership.
