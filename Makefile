format:
	uv run ruff format .

lint:
	uv run ruff check .

run:
	OPENAI_API_KEY=$$(cat .secret-openai) uv run streamlit run crashy.py

mypy:
	uv run mypy .

docker:
	docker build -t crashy .
	docker run --rm -e OPENAI_API_KEY=$$(cat .secret-openai) -p 8501:8501 crashy
