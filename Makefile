PY := .venv/bin/python

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '*.bak' -delete
	find . -name __pycache__ -delete
	rm -f .coverage

# DEPLOY
.PHONY: docs
docs:
	pip3 list | grep Sphinx || pip3 install -U sphinx
	cd docs && make html && cd -

.PHONY: dist
dist: docs
	$(PY) setup.py sdist

.PHONY: publish
publish: docs
	$(PY) setup.py sdist upload_docs --upload-dir=docs/build/html

