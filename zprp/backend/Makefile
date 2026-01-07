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

## Stop and remove backend containers
stop_backend:
	@echo ">>> Stopping backend and removing containers..."
	docker compose down -v --remove-orphans
	@echo ">>> Backend stopped and removed."

backend: start_backend import_backend
	@echo ">>> Backend is ready!"

