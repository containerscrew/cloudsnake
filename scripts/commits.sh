#!/usr/bin/env bash
set -euo pipefail

if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "ERROR: git-filter-repo is not installed."
  echo "Install it with: pip install git-filter-repo"
  exit 1
fi

# Conventional Commit regex:
# Allowed types: feat, fix, chore, refactor, docs, test, style, perf, build, ci
CONVENTIONAL_REGEX='^(feat|fix|chore|refactor|docs|test|style|perf|build|ci)(\(.+\))?: .+'

echo "Rewriting Git history..."

git filter-repo \
  --message-callback '
import re

msg = message.decode("utf-8").strip()

# If message does NOT match Conventional Commit format:
if not re.match(r"'"$CONVENTIONAL_REGEX"'", msg):
    new = f"chore: auto-fix non-conventional commit - {msg}\n"
    message = new.encode("utf-8")

return message
'

echo "✔ Git history rewritten successfully."
echo "⚠ If you want to push the rewritten history, use:"
echo "   git push --force --all"

