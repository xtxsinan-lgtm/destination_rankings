#!/usr/bin/env bash
set -euo pipefail

MSG="${1:-chore: update destination rankings data and pages}"

if [ -f "tools/build_seo.py" ]; then
  python3 tools/build_seo.py
fi

git add -A
if git diff --cached --quiet; then
  echo "No staged changes to commit."
else
  git commit -m "$MSG"
fi

git push origin HEAD
git log -1 --oneline
