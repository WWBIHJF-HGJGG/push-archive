#!/bin/bash
# Commit & push site to GitHub Pages; no-op if nothing changed.
set -e; cd "$(dirname "$0")"
git add -A
git diff --cached --quiet && { echo "deploy: nothing to commit"; exit 0; }
git commit -qm "update $(date '+%F %T %Z')"
git push -q origin main && echo "deploy: pushed"
