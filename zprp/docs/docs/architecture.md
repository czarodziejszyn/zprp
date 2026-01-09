# schemat blokowy rpzeplywu danych etc
# mapa wsyztskich folderow, co robia etc


# System architecture

## Data flow

## Modules
/zprp
├── backend/        # REST API and ML model integration
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
