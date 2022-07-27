SHELL := /bin/bash
.SHELLFLAGS := -o errexit -o nounset -o pipefail -c

.PHONY: run
run:
	source .venv/bin/activate && python -m cgpy.main

.PHONY: env
env:
	PYTHON_CFLAGS="-march=native -O3 -pipe" CONFIGURE_OPTS="--enable-optimizations --with-lto" pyenv install 3.10.5
	pyenv local 3.10.15
	python -m venv .venv
	source .venv/bin/activate && python -m pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf .venv
