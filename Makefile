SHELL:=/bin/sh
.PHONY: all

help: ## this help
	@awk 'BEGIN {FS = ":.*?## ";  printf "Usage:\n  make \033[36m<target> \033[0m\n\nTargets:\n"} /^[a-zA-Z0-9_-]+:.*?## / {gsub("\\\\n",sprintf("\n%22c",""), $$2);printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

run: ## Execute the cli locally using poetry
	poetry run python src/cloudsnake/__main__.py

deploy: ## Deploy package with twine
	twine upload dist/* --verbose

clean: ## Clean build files
	rm -rvf build/
	rm -rvf dist/
	rm -rvf *.egg-info

local-install: ## Install the package locally
	pip3 install .

local-uninstall: ## Uninstall the package locally
	pip3 uninstall awstools

lint: ## Lint python code
	pylint ecr_lifecycle

doctoc: ## Create table of contents with doctoc
	doctoc .