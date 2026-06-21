# Monitoring Rules

## Repository monitoring

Track these events in `INCIDENT_LOG.csv` or `EVIDENCE_LOG.md` when they occur:

- Security-relevant file changes.
- README/public claim changes.
- New network/API/login/backend functionality.
- CI/CD or GitHub Pages configuration changes.
- Discovery of private path, token pattern, raw log, or sensitive identifier.
- HIGH or CRITICAL finding.
- Human approval or denial for impactful action.

## Evidence rules

Evidence must be sanitized before public commit. Do not include secrets, private paths, hostnames, private IPs, account emails, tokens, keys, internal IDs, screenshots with sensitive data, or raw logs.

## Review cadence

Run a manual review before any release-state change and after any change to `index.html`, `styles.css`, `app.js`, README, AGENTS, or security docs.
