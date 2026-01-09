import time
import httpx
import statistics

BASE_URL = "http://localhost:8000"

def benchmark_endpoint(name, path, params, iterations=20):
    print(f"\n[Benchmarking {name}]")
    print(f"Path: {path} | Iterations: {iterations}")
    latencies = []
    
    with httpx.Client(base_url=BASE_URL, timeout=60.0) as client:
        try:
            # Warm-up request
            client.get(path, params=params)
        except Exception as e:
            print(f"ERROR: Server is not responding! {e}")
            return

        for i in range(iterations):
            start = time.perf_counter()
            response = client.get(path, params=params)
            end = time.perf_counter()
            
            if response.status_code == 200:
                latencies.append(end - start)
            else:
                print(f"Error in iteration {i}: Status {response.status_code}")

    if latencies:
        avg = statistics.mean(latencies)
        p95 = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
        rps = 1 / avg
        
        print(f"  -> Average latency: {avg:.4f} s")
        print(f"  -> P95 (worst-case): {p95:.4f} s")
        print(f"  -> Throughput (RPS): {rps:.2f} requests/sec")
    else:
        print("  -> Failed to collect benchmark data.")

def run_all_benchmarks():
    test_params = {"lat": 52.2297, "lon": 21.0122, "radius": 1000}
    
    # Database-only test (PostGIS)
    benchmark_endpoint("Database Only (Nearby)", "/nearby", test_params)
    
    # Full model test (Database + model computations)
    # This measures how much the model slows down the response compared to the DB alone
    benchmark_endpoint(
        "Full Model (Prices)",
        "/prices",
        {"lat": 52.2297, "lon": 21.0122}
    )
    
    # Chart generation test
    benchmark_endpoint("Chart Generation", "/chart", {}, iterations=5)

if __name__ == "__main__":
    run_all_benchmarks()
