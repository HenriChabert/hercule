.PHONY: tidy
tidy:
	black src/**/*.py
	isort src/**/*.py


.PHONY: seed
seed:
	python ./scripts/db.py seed