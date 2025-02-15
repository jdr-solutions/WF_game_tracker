.PHONY: run test coverage lint format ci help

run:
	python run.py

test:
	xvfb-run --auto-servernum pytest -v

coverage:
	xvfb-run --auto-servernum pytest --cov=wf_game_tracker -v --cov-report=term-missing

# Auto-format code with Black
format:
	black wf_game_tracker/

# Lint with Flake8
lint:
	flake8 wf_game_tracker

# Run GitHub Actions locally using act
ci:
	act

# Display available commands
help:
	@echo "Available commands:"
	@echo "  make run      - Run the application"
	@echo "  make test     - Run unit tests"
	@echo "  make coverage - Run tests with coverage"
	@echo "  make format   - Auto-format code with Black"
	@echo "  make lint     - Run flake8 (check only)"
	@echo "  make ci       - Run GitHub Actions locally with act"
	@echo "  make help     - Show this help message"
