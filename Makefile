.DEFAULT_GOAL := run_tests
SHELL := /bin/bash

.PHONY: run_tests
run_tests:
	source .venv/bin/activate && python -m pytest .

.PHONY: create_env
create_env:
	python -m venv .venv

.PHONY: remake_env
remake_env: delete_env create_env update_env

.PHONY: update_env
update_env:
	source .venv/bin/activate && python -m pip install -r requirements.txt

.PHONY: delete_env
delete_env:
	rm -rf .venv
