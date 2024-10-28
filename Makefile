format:
	uv run ruff format .

lint:
	uv run ruff check .

run:
	uv run streamlit run crashy.py

mypy:
	uv run mypy .
