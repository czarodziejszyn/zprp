.PHONY: start_backend import_backend stop_backend backend

## Build and start backend
start_backend:
	@echo ">>> Starting backend..."
	docker compose up -d --build
	@echo ">>> Backend started!"
	@echo "    API server: http://localhost:8000/"
	@echo "    Swagger docs: http://localhost:8000/docs"


## Import data into PostgreSQL
import_backend:
	@echo ">>> Importing data into PostgreSQL..."
	docker compose exec api bash -c "python -m db.import_data"
	@echo ">>> Data import completed!"


## Update API cache (overwrite api_cache.json)
update_api_cache:
	@echo ">>> Updating API cache..."
	docker compose exec api bash -c "python -m cache.save_cache"
	@echo ">>> API cache updated!"

## Stop and remove backend containers
stop_backend:
	@echo ">>> Stopping backend and removing containers..."
	docker compose down -v --remove-orphans
	@echo ">>> Backend stopped and removed."

backend: start_backend import_backend
	@echo ">>> Backend is ready!"



api_tests:
	pytest tests/test_api.py

fetch_api_tests:
	pytest tests/test_fetch_warsaw_api.py


cache_tests:
	pytest tests/test_cache.py



