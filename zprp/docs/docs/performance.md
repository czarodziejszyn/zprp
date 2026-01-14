# Performance Benchmarks

## Test Environment
- Backend: FastAPI
- Database: PostgreSQL + PostGIS
- Hardware: local machine
- Benchmark tool: custom Python script (httpx)
- Iterations: 20 per endpoint (5 for chart generation)

All benchmarks were executed locally against a running backend instance with preloaded data.

## Tested Endpoints
- `/nearby` – database-only spatial query
- `/prices` – full processing pipeline (database + model computations)
- `/chart` – chart generation endpoint

## Running the Benchmarks
The following command starts the backend, waits for initialization, runs all benchmarks, and then shuts the backend down:
```
make backend_benchmark
```

## Results

### Database Only (Nearby)
* Average latency: 138 ms
* P95 latency: 155 ms
* Throughput: ~7.3 requests/sec

### Full Model (Prices)
* Average latency: 2.11 s
* P95 latency: 2.72 s
* Throughput: ~0.47 requests/sec

### Chart Generation
* Average latency: 21 ms
* P95 latency: 22 ms
* Throughput: ~47.4 requests/sec

## Observations
- Database-only queries are fast and stable.
- Model computation dominates the overall request latency. It is primary performance bottleneck.
- Performance variance is low for most endpoints, as shown by relatively small differences between average and P95 latencies.
- Chart generation is efficient.
