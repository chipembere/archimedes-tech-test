format:
	poetry run black tests/ src/

test:
	poetry run pytest

main:
	poetry run python src/main.py