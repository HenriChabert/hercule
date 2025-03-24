.PHONY: tidy
tidy:
	black src/**/*.py
	isort src/**/*.py