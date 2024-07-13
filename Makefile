SHELL:=/bin/sh
.PHONY: all

app_name="cloudsnake"

help: ## this help
	@awk 'BEGIN {FS = ":.*?## ";  printf "Usage:\n  make \033[36m<target> \033[0m\n\nTargets:\n"} /^[a-zA-Z0-9_-]+:.*?## / {gsub("\\\\n",sprintf("\n%22c",""), $$2);printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

run: ## Execute the cli locally using poetry
	poetry run python src/cloudsnake/__main__.py

install: ## Install dependencies
	poetry install

build: ## Build project using poetry
	poetry build

run-coverage: ## Run pytest with coverage
	poetry run pytest --cov=cloudsnake tests/

publish: ## Publish package to pypi.org
	poetry publish --build

publish-to-test: ## Publish to test pypip
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish --build -r testpypi

clean: ## Clean build files
	rm -rvf dist/

doctoc: ## Create table of contents with doctoc
	doctoc .

pre-commit-install: ## Install pre-commit
	pre-commit install

pre-commit-uninstall: ## Uninstall pre-commit
	pre-commit uninstall

run-pre-commit: ## Run pre-commit locally
	pre-commit run -a

pipx-local-install: ## Install the package locally using pipx
	pipx install . --force

pipx-upgrade: ## Upgrade package
	pipx upgrade ${app_name}

pipx-uninstall: ## Uninstall package
	pipx uninstall ${app_name}

init-git-cliff: # Init git cliff
	git-cliff --init

generate-changelog: ## Generate changelog
	git cliff -o CHANGELOG.md

run-tests: ## Run pytest using poetry
	poetry run pytest -v -s

poetry-cache-clear: ## Clear poetry cache
	poetry cache clear pypi --all

export-requirements: ## Export requirements.txt using poetry
	poetry export -f requirements.txt --output requirements.txt

init-gitmoji: ## Init gitmoji (sudo npm i -g gitmoji-cli)
	gitmoji --init
