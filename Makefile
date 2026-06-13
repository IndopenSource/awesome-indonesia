.PHONY: update lint validate check

update:
	python3 scripts/update-readme.py

lint:
	npx --yes markdownlint-cli --config .markdownlint.json README.md CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md

validate:
	python3 scripts/validate-catalog.py

check: validate update lint
