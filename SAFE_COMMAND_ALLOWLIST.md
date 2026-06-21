# Safe Command Allowlist

Commands below are proposals for local authorized review. Do not execute without explicit approval in the current turn.

## Read-only inventory

```powershell
Get-ChildItem -Force
Get-ChildItem -Recurse -File -Force | Select-Object FullName,Length,LastWriteTime
git status --short --branch
git remote -v
```

## Static security checks

```powershell
rg -n "C:\\Users|file:///|sk-|ghp_|token|password|secret|private key|BEGIN .* KEY" .
rg -n "innerHTML|outerHTML|insertAdjacentHTML|eval\(|Function\(|document.write|localStorage|sessionStorage" app.js index.html
node --check app.js
git diff --check
```

## Local preview only

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Local preview must stay bound to `127.0.0.1` unless a human explicitly approves otherwise.
