#!/usr/bin/env bash
set -euo pipefail

OWNER="aisamuraiagent-source"
REPO="FCCSecurity-Public"
PROJECT_TITLE="FCCSecurity Public Release Gate"
REPO_FULL="${OWNER}/${REPO}"
FALLBACK_DOC="docs/GITHUB_PROJECT_UI_SETUP.md"
ISSUES=(6 7 8 9 10)

log() {
  printf '[public-release-gate-project] %s\n' "$*"
}

fail_with_fallback() {
  log "$1"
  log "Fallback: ${FALLBACK_DOC}"
  exit 0
}

if ! command -v gh >/dev/null 2>&1; then
  fail_with_fallback "gh CLI is unavailable; Project V2 automation skipped."
fi

if ! gh auth status >/dev/null 2>&1; then
  fail_with_fallback "gh CLI is not authenticated; Project V2 automation skipped."
fi

if ! gh repo view "${REPO_FULL}" >/dev/null 2>&1; then
  fail_with_fallback "Repository access check failed for ${REPO_FULL}; Project V2 automation skipped."
fi

log "Attempting to create or locate Project V2: ${PROJECT_TITLE}"

# GitHub Project V2 support varies by gh version and token scopes.
# This script intentionally avoids printing tokens and degrades to the UI fallback.

PROJECT_NUMBER=""
if gh project list --owner "${OWNER}" --format json >/tmp/fccsecurity_projects.json 2>/tmp/fccsecurity_project_err.log; then
  PROJECT_NUMBER="$(python - <<'PY'
import json
from pathlib import Path
needle = "FCCSecurity Public Release Gate"
data = json.loads(Path('/tmp/fccsecurity_projects.json').read_text())
for item in data.get('projects', []):
    if item.get('title') == needle:
        print(item.get('number', ''))
        break
PY
)"
else
  fail_with_fallback "Unable to list Project V2 items with gh; token may lack project scope."
fi

if [ -z "${PROJECT_NUMBER}" ]; then
  if gh project create --owner "${OWNER}" --title "${PROJECT_TITLE}" --format json >/tmp/fccsecurity_project_created.json 2>/tmp/fccsecurity_project_create_err.log; then
    PROJECT_NUMBER="$(python - <<'PY'
import json
from pathlib import Path
data = json.loads(Path('/tmp/fccsecurity_project_created.json').read_text())
print(data.get('number', ''))
PY
)"
  else
    fail_with_fallback "Unable to create Project V2 with gh; use manual UI setup."
  fi
fi

if [ -z "${PROJECT_NUMBER}" ]; then
  fail_with_fallback "Project number could not be resolved after create/list."
fi

log "Project number: ${PROJECT_NUMBER}"

for issue in "${ISSUES[@]}"; do
  issue_url="https://github.com/${REPO_FULL}/issues/${issue}"
  if gh project item-add "${PROJECT_NUMBER}" --owner "${OWNER}" --url "${issue_url}" >/dev/null 2>/tmp/fccsecurity_project_add_err.log; then
    log "Added issue #${issue}"
  else
    log "Could not add issue #${issue}; continue and use manual fallback if needed."
  fi
done

cat <<EOF
Project automation completed as far as supported by the available gh installation and token scope.

Project:
${PROJECT_TITLE}

Repository:
${REPO_FULL}

If fields/views were not created automatically, finish setup using:
${FALLBACK_DOC}
EOF
