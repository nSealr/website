.PHONY: setup test lint audit docs ci

setup:
	@echo "No setup required until the Astro scaffold is introduced."

test:
	python3 scripts/verify_repo.py
	python3 -m unittest discover -s tests

lint:
	python3 scripts/verify_repo.py
	python3 -m compileall -q scripts tests

audit:
	python3 scripts/verify_repo.py
	python3 scripts/validate_site.py

docs:
	python3 scripts/verify_repo.py
	python3 scripts/validate_site.py

ci: setup test lint audit docs
