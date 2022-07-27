SHELL := /bin/bash
.SHELLFLAGS := -o errexit -o nounset -o pipefail -c

env:
	python -m venv .venv
	source .venv/bin/activate && python -m pip install -r requirements.txt

clean:
	rm -rf .venv
