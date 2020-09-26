PYTHON_VERSIONS = \
	3.6 \
	3.8 \

.PHONY: $(addprefix env-,$(PYTHON_VERSIONS))
$(addprefix env-,$(PYTHON_VERSIONS)):
	$(eval PY_VERSION := $(subst env-,,$@))
	$(eval PY := $(shell which python$(PY_VERSION)))
	@if [ -z "$(PY)" ]; then echo "\e[31mpython$(PY_VERSION) not found\e[0m" ; exit 1; fi
	@poetry env use $(PY)

.PRECIOUS: poetry.lock.%
poetry.lock.%: pyproject.toml
	@($(MAKE) env-$*)
	@-cp -f $@ poetry.lock
	@poetry install
	@cp -f poetry.lock $@

.PHONY: setup
setup: $(addprefix poetry.lock.,$(PYTHON_VERSIONS))


test-%: poetry.lock.% env-%
	@echo "\e[1m\e[96mRunning tests with python$*\e[0m"
	@poetry run pytest -q -rs -c pytest.ini

.PHONY: test
test: $(addprefix test-,$(PYTHON_VERSIONS))

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: format
format:
	isort -y
	black ./
