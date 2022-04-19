format:
	poetry run black tests/ src/

test:
	poetry run pytest