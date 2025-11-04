install:
	poetry install --no-root

run:
	docker compose up --build

clear:
	docker compose down --remove-orphans