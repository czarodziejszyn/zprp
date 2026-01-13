# System architecture

## Data flow

1. User selects address in Warsaw using the web application.
2. Frontend application converts selected address into geographic coordinates.
3. Frontend sends coordinates to the backend API.
4. Backend triggers machine learning model to predict the apartment price per square meter for given location.
5. At the same time, backend selects offers from within 500m radius of given coordinates and calculates average price per square meter.
6. Backend exposes the following data via its API:
  - predicted price per square meter,
  - real price per square meter,
  - feature importances chart.
7. Frontend retrieves data from backend API and displays it to the user.

## Modules
```
/zprp
├── backend/        # API and ML model integration
│   ├── api/        # Backend API request handlers
│   ├── cache/      # Warsaw API response caching layer using a local JSON file
│   ├── db/         # Database connections and schema management
│   └── model_use/  # Implementation of ML model within the API
├── data/           # Raw JSON data - cache files
├── data_science/   # ML logic and analyses
├── frontend/       # Interactive web application
├── geocoding/      # Geocoding module (address → coordinates)
├── logger/         # Monitoring and logging
├── notebooks/      # Jupyter Notebooks for data exploration
├── reports/        # Reports and visualizations
├── scraping/       # Web scraper (Otodom)
└── tests/          # Unit and integration tests
```
