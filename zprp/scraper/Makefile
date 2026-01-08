.PHONY: build_scraper run_scraper stop_scraper scrape

## Build scraper Docker image
build_scraper:
	@echo ">>> Building scraper Docker image..."
	docker compose build --no-cache
	@echo ">>> Scraper image built."

## Run scraper (creates .json in data/raw)
run_scraper:
	@echo ">>> Running scraper..."
	docker compose up
	@echo ">>> Scraping finished."

## Stop and remove scraper containers
stop_scraper:
	@echo ">>> Stopping scraper containers..."
	docker compose down
	@echo ">>> Scraper stopped."

## Full scraping pipeline
scrape: build_scraper run_scraper stop_scraper
	@echo ">>> Scraping pipeline completed!"
