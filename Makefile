# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = poetry run sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build
LONG_RERUN    = 12h
SHORT_RERUN   = 30m

.PHONY: Makefile

build: always-run .cache/make/long-pre-commit .cache/make/long-poetry .cache/make/doc .cache/make/run .cache/make/test  # Build the project (default target if you simply run `make` without targets)
.PHONY: build

always-run:
	@mkdir -p .cache/make
.PHONY: always-run

# Remove cache files if they are older than the configured time, so the targets will be rebuilt
# "fd" is a faster alternative to "find": https://github.com/sharkdp/fd
	@fd --changed-before $(LONG_RERUN) long .cache/make --exec-batch rm '{}' ;
	@fd --changed-before $(SHORT_RERUN) short .cache/make --exec-batch rm '{}' ;

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo 'Or choose one of the following targets:'
	@cat Makefile | egrep '^[a-z0-9-]+: *.* +#' | sed -E -e 's/:.+# */@ /g' | sort | awk -F@ '{printf "  \033[1;34m%-10s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo 'Run 'make -B' or 'make --always-make' to force a rebuild of all targets'
.PHONY: help

pre-commit: # Update and install pre-commit hooks
	-rm .cache/make/long-pre-commit
	$(MAKE)
.PHONY: pre-commit

.cache/make/long-pre-commit: .pre-commit-config.yaml .pre-commit-hooks.yaml
	pre-commit autoupdate
	pre-commit install --install-hooks
	pre-commit install --hook-type commit-msg
	pre-commit gc
	touch .cache/make/long-pre-commit
	-rm .cache/make/run

poetry: # Update dependencies
	-rm .cache/make/long-poetry
	$(MAKE)
.PHONY: poetry

.cache/make/long-poetry: pyproject.toml
	poetry update
	poetry install

# Update the requirements for Read the Docs, adding Nitpick as well (autodoc needs it)
# "rg" is a faster alternative to "grep": https://github.com/BurntSushi/ripgrep
	echo "# NOTE: generated by the Makefile" > docs/requirements.txt
	echo "# This will be installed by Read the Docs, from the root folder" >> docs/requirements.txt
	poetry run python3 -m pip freeze | rg -i -e sphinx -e pygments | sort -u >> docs/requirements.txt

	touch .cache/make/long-poetry
	-rm .cache/make/run

doc: docs/*/* *.rst *.md # Build documentation only (use force=1 to force a rebuild)
ifdef force
	-rm -rf .cache/make/*doc* docs/_build docs/source
endif
	$(MAKE) .cache/make/short-doc-source .cache/make/doc-defaults .cache/make/doc .cache/make/short-doc-link-check
.PHONY: doc

.cache/make/short-doc-source:
	-rm -rf docs/source
	poetry run sphinx-apidoc --force --module-first --separate --implicit-namespaces --output-dir docs/source src/nitpick/
	touch .cache/make/short-doc-source

.cache/make/doc-defaults: docs/generate_rst.py styles/*/*
	poetry run python3 docs/generate_rst.py
	touch .cache/make/doc-defaults

# $(O) is meant as a shortcut for $(SPHINXOPTS).
.cache/make/doc: docs/*/* *.rst *.md .cache/make/short-doc-source .cache/make/doc-defaults
	@$(SPHINXBUILD) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	$(MAKE) .cache/make/short-doc-link-check
	touch .cache/make/doc

# Detect broken links on the documentation
.cache/make/short-doc-link-check:
	$(SPHINXBUILD) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -blinkcheck
	touch .cache/make/short-doc-link-check

.cache/make/run: .github/*/* .travis/*/* docs/*.py src/*/* styles/*/* tests/*/* nitpick-style.toml
	pre-commit run --all-files
	poetry run flake8
	touch .cache/make/run

nitpick: # Run the nitpick pre-commit hook to check local style changes
	pre-commit run --all-files nitpick-local
.PHONY: nitpick

flake8: # Run flake8 to check local style changes
	poetry run flake8 --select=NIP
.PHONY: flake8

test: # Run tests (use failed=1 to run only failed tests)
	-rm .cache/make/test
	$(MAKE) .cache/make/test
.PHONY: test

.cache/make/test: .cache/make/long-poetry src/*/* styles/*/* tests/*/*
ifdef failed
	poetry run pytest --failed
else
	-rm .pytest/failed
	# Run doctests in a separate command.
	# It was breaking a test because the Nitpick Flake8 plugin was being initialized twice, raising the error:
	# optparse.OptionConflictError: option --nitpick-offline: conflicting option string(s): --nitpick-offline
	poetry run pytest --doctest-modules src/
	poetry run pytest
endif
	touch .cache/make/test

ci: # Simulate CI run (force clean docs and tests, but do not update pre-commit nor Poetry)
	-rm -rf .cache/make/*doc* .cache/make/run .cache/make/test docs/_build docs/source
	$(MAKE) force=1
.PHONY: ci
