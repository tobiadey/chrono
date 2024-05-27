.PHONY: test

# Run unit tests
test:
	FLASK_ENV=test pytest app

# Check code style
lint-flake8:
	flake8 app

lint-types:
	mypy --package app

lint: lint-types lint-flake8

# Sort imports and format code
format-isort:
	isort .

format-black:
	black .

format: format-black format-isort

# Start the Core server with debug mode enabled
server-core:
	@echo "Starting Core Server in Development Mode..."
	@. env/bin/activate; cd app/api; export FLASK_APP=app.py; export FLASK_ENV=development; flask run --port 5001

# Start the BFF server with debug mode enabled
server-bff:
	@echo "Starting BFF Server in Development Mode..."
	@. env/bin/activate; cd app/bff; export FLASK_APP=app.py; export FLASK_ENV=development; flask run --port 5000

# Create virtual environment
venv-create:
	python3.8 -m venv env

# Prepare virtual environment
venv: venv-create
	@echo "\nUse '. env/bin/activate' to activate and 'make install' to install all dependencies"

# Install dependencies
install:
	pip install -r requirements.txt