.PHONY: setup dev build check validate test lint ci clean

setup:
	pnpm install --frozen-lockfile

dev:
	pnpm run dev

build:
	pnpm run build

check:
	pnpm exec astro check

validate:
	python3 scripts/validate_site.py

test:
	python3 -m unittest discover -s tests

lint:
	python3 scripts/verify_repo.py
	python3 -m compileall -q scripts tests

ci: setup check build validate test lint

clean:
	rm -rf dist .astro node_modules
