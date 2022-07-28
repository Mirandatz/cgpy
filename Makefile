SHELL := /bin/bash
.SHELLFLAGS := -o errexit -o nounset -o pipefail -c
.DEFAULT_GOAL := run 

.PHONY: run
run:
	source .venv/bin/activate && python -m cgpy.main

.PHONY: env
env:
	rm -rf .venv
	python -m venv .venv
	source .venv/bin/activate && python -m pip install -r requirements.txt


.PHONY: install_pyenv_deps
install_pyenv_deps:
	sudo apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
		build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
		libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev \
		\
		git libx11-dev


.PHONY: install_pyenv
install_pyenv:
	rm -rf ~/.pyenv
	curl https://pyenv.run | bash
	PYTHON_CFLAGS="-march=native -O3 -pipe" CONFIGURE_OPTS="--enable-optimizations --with-lto" pyenv install 3.10.5
	pyenv local 3.10.5

.PHONY: install_python
install_python:
	PYTHON_CFLAGS="-march=native -O3 -pipe" CONFIGURE_OPTS="--enable-optimizations --with-lto" pyenv install 3.10.5
	pyenv local 3.10.5

.PHONY: install_everything
install_everything: install_pyenv_deps install_pyenv install_python env
