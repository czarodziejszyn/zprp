# API reference
This module serves as the central communication hub. It consists of two main parts:
1. Public API (FastAPI): Endpoints consumed by the frontend and model.
2. Data Integration (Warsaw API): A client for fetching data from Warsaw Open Data sources.

## Public API endpoints:
### Endpoints for model:
* `GET /nearby`: Returns counts of objects (parks, stops, etc.) within a specified radius of a location.

* `GET /real_price`: Calculates the average market price per square meter in a specific area based on current database record.

### Endpoints for frontend:
* `GET /prices`: Returns both the predicted price (from the ML model) and the actual average price for a given coordinate.

* `GET /chart`: Generates a dynamic comparison chart (PNG) and serves it directly as a file response.

## Warsaw Open Data Integration:
### Resiliency Features
To ensure stable data flow, the integration includes:
* Retries with Exponential Backoff: Automatically retries failed requests up to 3 times with increasing delays.
* Pydantic Validation: All incoming data is mapped to WarsawApiObj to ensure consistent data types across the pipeline.
* Unified Interface: Different Warsaw API formats (WFS Store, Datastore Search) are normalized into a single coordinate-based format.

## API flow:
API module is organized into three parts:
1. Public API Layer (`main.py`): Acts as the entry point for all external requests.
2. Universal Fetching Layer (`fetch_warsaw_api.py`): A centralized engine used by all data parsers. It handles the "heavy lifting" of network communication with the Warsaw Open Data API, including authentication, retries, and error handling.
3. Specialized Parsing Layer (e.g., `nature.py`, `accommodations.py`): Individual modules dedicated to specific types of urban data. Each of these modules imports the universal fetcher, but contains unique logic to transform raw JSON responses into the unified WarsawApiObj format.