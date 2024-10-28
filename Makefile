format:
	uv run ruff format .

lint:
	uv run ruff check .

run:
	uv run python3 trial.py
