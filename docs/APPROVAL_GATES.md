# Approval Gates

## Gate 1 - Read-only local inventory

Allowed only after explicit approval. Output must summarize structure and Git state without changing files.

## Gate 2 - Network or GitHub read

Allowed only after explicit approval. Use least privilege and record source URLs or repository paths reviewed.

## Gate 3 - File modification

Allowed only after explicit approval. Patch must state files changed, reason, validation, and residual risk.

## Gate 4 - CI/CD or release

Blocked by default. Requires explicit approval because it can affect publication or automation.

## Gate 5 - HIGH or CRITICAL finding

Stop normal flow. Document finding, impact, evidence, recommended correction, validation test, and enforcement decision before continuing.

## Gate 6 - Secret or sensitive data

Do not print, store, copy, or publish. Ask for a safe destination and use a secret-aware workflow only when necessary.
