# Real Estate Scraping
This module is responsible for the automated extraction of real estate listings from Otodom portal. It uses Selenium WebDriver to navigate through paginated search results and collect raw property data.


## Pipeline execution - `main.py`:
1. Initialize WebDriver: Sets up the browser with Docker-ready options.
2. Scrape listings: Iterates through pages while filtering out advertisements and incomplete offers.
3. Data Persistence: Stores the final list as a structured JSON file for further processing.


## Scrapping implementation - `scrapping.py`
The module utilizes a headless Chrome browser to handle:
* Dynamic Web Crawling: Manages JavaScript rendering, cookie consent, and pagination logic.
* Data Extraction and Cleaning: For every listing identified by the <article> tag, the scraper extracts:
    * Identifying Info: Title and unique URL (used for de-duplication).
    * Price: Total price and calculated price per m2.
    * Total area(m2): Extracted using Regex.
    * Location: Raw address string for future geocoding.



## Technical configuration
The scraper relies on several environment variables. The most critical are:
* `CHROME_BINARY_PATH` and `CHROMEDRIVER_PATH`: Paths to the browser engine and driver. These are pre-configured for the Docker environment and should not be modified manually. 
* `MAX_OFFER_PAGES`: Limit for the number of pages to crawl.
* `OTODOM_URL`: The base search URL for the targeted listings.