NAME=restrek
OS=$(shell uname -s)

PYTHON=python
PIP=pip

all: clean

test:
	python setup.py test

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	rm -rf lib/ansible.egg-info/
	find . -type f -name "pytest_runner-*.egg" -delete
	@echo "Cleaning up compiled code"
	find . -type f -regex ".*\.py[co]$$" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".tmp" -prune -exec rm -rf '{}' \;
	find . -type d -name .cache -prune -exec rm -rf '{}' \;
	find . -type d -name .eggs -prune -exec rm -rf '{}' \;

build:
	$(PYTHON) setup.py build

install: build
	$(PIP) install -r requirements.txt
	$(PYTHON) setup.py install
