"""
refined_benchmark.py - Benchmark dla ulepszonych wersji A4, A11, A12.
"""
import os
import sys
import csv
import time
import multiprocessing

# Ścieżka do bazowego folderu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_DIR = os.path.join(BASE_DIR, '..', 'initial_test')
sys.path.append(ORIGINAL_DIR)

from shapes import get_all_shapes, get_radius
from refined_algorithms import ALGORITHMS_REFINED

TIMEOUT_S = 300

def _worker(q, algo_name, polygon_wkt, radius):
    try:
        from shapely.wkt import loads
        from refined_algorithms import ALGORITHMS_REFINED
        from coverage import sample_interior, coverage_pct
        
        poly = loads(polygon_wkt)
        func = ALGORITHMS_REFINED[algo_name]
        
        t0 = time.perf_counter()
        centers = func(poly, radius)
        elapsed = time.perf_counter() - t0
        
        test_pts = sample_interior(poly, n=2000, seed=0)
        cov = coverage_pct(test_pts, centers, radius)
        
        q.put(('ok', len(centers), elapsed, cov))
    except Exception as e:
        import traceback
        traceback.print_exc()
        q.put(('error', 0, 0.0, 0.0))

def run_one(algo_name, polygon, radius):
    from shapely.wkt import dumps
    wkt = dumps(polygon)
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=_worker, args=(q, algo_name, wkt, radius), daemon=True)
    p.start()
    p.join(TIMEOUT_S)
    
    if p.is_alive():
        p.terminate()
        return 'DNF', 0.0, 0.0
    if not q.empty():
        status, n, t, cov = q.get()
        if status == 'ok': return n, t, cov
    return 'ERR', 0.0, 0.0

def main():
    shapes = get_all_shapes()
    algos = list(ALGORITHMS_REFINED.keys())
    
    os.makedirs(os.path.join(BASE_DIR, 'results'), exist_ok=True)
    out_csv = os.path.join(BASE_DIR, 'results', 'refined_results.csv')
    
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['shape_id', 'shape_name', 'algorithm', 'n_circles', 'time_s', 'coverage_pct'])
        writer.writeheader()
        
        for sid, sname, poly in shapes:
            radius = get_radius(poly)
            print(f"\nEvaluating {sid} | {sname} (r={radius})")
            for algo in algos:
                n, t, cov = run_one(algo, poly, radius)
                print(f"  {algo:<15} : {n:>4} circles | {t:>6.2f}s | cov={cov:.1f}%")
                writer.writerow({
                    'shape_id': sid, 'shape_name': sname, 'algorithm': algo,
                    'n_circles': n, 'time_s': f"{t:.3f}", 'coverage_pct': f"{cov:.2f}"
                })
                f.flush()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
