.PHONY: run test coverage lint format help

run:
	python run.py

test:
	xvfb-run --auto-servernum pytest -v

coverage:
	pytest --cov=wf_game_tracker -v --cov-report=term-missing

# Auto-format code with Black
format:
	black wf_game_tracker/

# Lint with Flake8
lint: format
	flake8 wf_game_tracker

# Display available commands
help:
	@echo "Available commands:"
	@echo "  make run      - Run the application"
	@echo "  make test     - Run unit tests"
	@echo "  make coverage - Run tests with coverage"
	@echo "  make format   - Auto-format code with Black"
	@echo "  make lint     - Run flake8 (after formatting)"
	@echo "  make help     - Show this help message"
