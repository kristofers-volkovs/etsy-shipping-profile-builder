
run:
	uv run python src/main.py

check:
	uv run ruff format src/ && \
	uv run ruff check src/ --fix && \
	uv run mypy --package src --namespace-packages
