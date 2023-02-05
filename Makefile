check: test lint 

test: test-runflake8 test-pytest

clean:
	rm -rf dist/*

test-runflake8:
	tests/run_flake8/Run.sh

test-pytest:
	coverage erase
	coverage run -m unittest discover -v  # tests/test_*.py
	coverage xml --fail-under 90

codecov:
	codecov


lint: mypy flake8

flake8:
	flake8 --version
	flake8 --ignore=E501,W503 .

isortify:
	isort .

blacken:
	black .

mypy:
	# Temporarily check only package directory
	mypy --strict flake8_no_implicit_str_concat_in_list/



sdist: clean
	hatch build -t sdist

wheel: clean
	hatch build -t wheel

publish_repository ?= test
publish: sdist wheel
	hatch publish -r $(publish_repository)

# Do not add to devdependencies because different platforms install
# different packages
publish-installdeps:
	pip install hatch
