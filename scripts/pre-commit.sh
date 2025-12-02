#!/usr/bin/env bash
set -euo pipefail

separator() {
    echo -e "\n--- $1 ---"
}

separator "Running pre-commit hooks"
pre-commit run -a --show-diff-on-failure

# separator "Scanning for secrets"
# gitleaks git -v

# separator "Running ruff format and ruff check"
ruff format
ruff check

# separator "Running pytest"
# poetry run pytest -v
