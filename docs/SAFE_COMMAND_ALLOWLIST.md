# Safe Command Allowlist

Commands below are proposals for local authorized review. Do not execute without explicit approval in the current turn.

## Read-only inventory

```powershell
Get-ChildItem -Force
Get-ChildItem -Recurse -File -Force | Select-Object FullName,Length,LastWriteTime
git status --short --branch
git remote
$remote = git config --get remote.origin.url
if ($remote) { $remote -replace '://[^/@]+@', '://<redacted>@' -replace '(ghp_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]+)', '<redacted>' }
```

Do not log raw remote URLs. Some environments embed usernames or personal access tokens in Git remote configuration.

## Static security checks

```powershell
$secretPattern = 'ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9][A-Za-z0-9_-]{18,}|-----BEGIN (RSA |OPENSSH |EC |DSA |)?PRIVATE KEY-----'
rg -n $secretPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'
$privatePathPattern = 'C:' + '\\Users\\|file:///C:/Users|://[^/@\s]+@'
rg -n $privatePathPattern README.md AGENTS.md SECURITY.md docs index.html app.js styles.css --glob '!docs/security-scans/**' --glob '!docs/SAFETY_TEST_PLAN.md' --glob '!docs/SAFE_COMMAND_ALLOWLIST.md'
rg -n "innerHTML|outerHTML|insertAdjacentHTML|eval\(|new Function|document.write" app.js index.html styles.css
node --check app.js
git diff --check
```

## Local preview only

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Local preview must stay bound to `127.0.0.1` unless a human explicitly approves otherwise.
