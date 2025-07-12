poetry_install_dev:
	poetry install --with test --sync

poetry_install:
	poetry install --sync

build:
	docker compose build

up:
	docker compose up -d

up_build:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

migrate_db:
	alembic upgrade head

dev:
	@echo "Starting MySQL container..."
	@docker compose up -d --build mysql-db
	@echo "Applying migrations..."
	@./config/init_db/init_db.sh
	@echo "Starting Uvicorn..."
	@trap 'docker compose down --remove-orphans' INT TERM EXIT; \
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

test_watch:
	ENV=test ptw --runner 'pytest --ff $(extra)'

test_parallel:
	ENV=test pytest --cov=src --numprocesses auto --dist loadfile --max-worker-restart 0 $(extra)

test_last_failed:
	ENV=test ptw --runner 'pytest --ff --lf $(extra)'

test_coverage:
	coverage report --omit=tests/*
