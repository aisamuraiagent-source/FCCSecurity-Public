# Security Scope

## Repository

- Project: `FCCSecurity-Public`
- Repository: `aisamuraiagent-source/FCCSecurity-Public`
- Default branch: `main`
- Environment: public static preview and authorized local/dev review

## In scope

- Static app source: `index.html`, `styles.css`, `app.js`
- Static hosting control: `.nojekyll`
- Public docs: `README.md`, `AGENTS.md`, `SECURITY.md`, security evidence files
- Defensive review of repository-only code, copy, links, and documentation consistency

## Out of scope

- External targets and public network scanning
- Private repos not named in the current approved task
- Secrets, tokens, keys, credentials, session material, payment data, account email, or live sensitive logs
- Malware, persistence, evasion, exploit execution, credential capture, exfiltration, or bypass instructions
- OS-level changes, permission changes, installs, CI/CD edits, deletes, pushes, or releases without explicit approval

## Current risk boundary

The public project is documented as a static local-first preview with no backend, database, login, external API, telemetry, credential collection, or production automation. Any future feature that changes that boundary requires this scope to be updated before implementation.
