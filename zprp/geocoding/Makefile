.PHONY: nominatim_start nominatim_logs nominatim_stop build_geocoding run_geocoding geocode

NOMINATIM_CONTAINER = nominatim-warsaw
NOMINATIM_PORT = 6080
NOMINATIM_IMAGE = peterevans/nominatim:latest
NOMINATIM_PBF_URL = https://download.bbbike.org/osm/bbbike/Warsaw/Warsaw.osm.pbf

## Start Nominatim server
nominatim_start:
	@echo ">>> Starting Nominatim server..."
	@docker run -d \
		-p $(NOMINATIM_PORT):8080 \
		-e NOMINATIM_PBF_URL="$(NOMINATIM_PBF_URL)" \
		-e POSTGRES_PASSWORD="haslo" \
		--name $(NOMINATIM_CONTAINER) \
		$(NOMINATIM_IMAGE) || true
	@echo ">>> Nominatim will be available at http://localhost:$(NOMINATIM_PORT)/"


## Follow Nominatim logs. Press Ctrl+C to exit
nominatim_logs:
	@echo ">>> Following Nominatim logs..."
	docker logs -f $(NOMINATIM_CONTAINER)

## Stop Nominatim server
nominatim_stop:
	@echo ">>> Stopping Nominatim server..."
	@docker stop $(NOMINATIM_CONTAINER) || true
	@echo ">>> Nominatim stopped."


## Build geocoding Docker image (no cache)
build_geocoding:
	@echo ">>> Building geocoding Docker image..."
	docker compose build --no-cache
	@echo ">>> Geocoding image built."

## Run geocoding (creates .json in data/processed)
run_geocoding:
	@echo ">>> Running geocoding..."
	docker compose up
	@echo ">>> Geocoding finished."

## Full geocoding pipeline:
## start Nominatim → geocode → stop Nominatim
geocode: nominatim_start build_geocoding run_geocoding nominatim_stop
	@echo ">>> Geocoding pipeline completed!"