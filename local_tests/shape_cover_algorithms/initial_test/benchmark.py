"""
benchmark.py - Runs all algorithms on all shapes.

Usage:  python benchmark.py
Output: results/results.csv
Timeout: 300s (5 minutes) per algorithm per shape
"""
import os
import sys
import csv
import math
import time
import multiprocessing
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TIMEOUT_S = 300
N_TEST_PTS = 2000


def _worker(q, algo_name, polygon_wkt, radius, seed):
    """Runs in a child process."""
    try:
        from shapely.wkt import loads
        from algorithms import ALGORITHMS
        from coverage import sample_interior, coverage_pct

        polygon = loads(polygon_wkt)
        func = ALGORITHMS[algo_name]

        t0 = time.perf_counter()
        centers = func(polygon, radius, seed)
        elapsed = time.perf_counter() - t0

        test_pts = sample_interior(polygon, n=N_TEST_PTS, seed=0)
        cov = coverage_pct(test_pts, centers, radius)

        q.put(('ok', len(centers), elapsed, cov))
    except Exception:
        traceback.print_exc()
        q.put(('error', 0, 0.0, 0.0))


def run_one(algo_name, polygon, radius, seed=42, timeout=TIMEOUT_S):
    """Run one algorithm with timeout.
    Returns: (n_circles, time_s, coverage_pct, dnf_bool)
    """
    from shapely.wkt import dumps
    polygon_wkt = dumps(polygon, rounding_precision=8)

    q = multiprocessing.Queue()
    p = multiprocessing.Process(
        target=_worker,
        args=(q, algo_name, polygon_wkt, radius, seed),
        daemon=True,
    )
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return 0, float(timeout), 0.0, True  # DNF

    if not q.empty():
        status, n, elapsed, cov = q.get()
        if status == 'ok':
            return n, elapsed, cov, False

    return 0, 0.0, 0.0, True  # Error = DNF


def main():
    from shapes import get_all_shapes, get_radius
    from algorithms import ALGORITHMS

    shapes = get_all_shapes()
    algo_names = list(ALGORITHMS.keys())

    total = len(shapes) * len(algo_names)
    done = 0

    print("\n" + "=" * 65)
    print(f"  BENCHMARK: {len(shapes)} shapes x {len(algo_names)} algorithms = {total} tests")
    print(f"  Timeout per test: {TIMEOUT_S}s")
    print("=" * 65 + "\n")

    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    csv_path = os.path.join(HERE, 'results', 'results.csv')
    fieldnames = ['shape_id', 'shape_name', 'algorithm',
                  'n_circles', 'coverage_pct', 'time_s', 'status']

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for shape_id, shape_name, polygon in shapes:
            radius = get_radius(polygon)
            minx, miny, maxx, maxy = polygon.bounds
            diag = math.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)
            print("\n" + "-" * 65)
            print(f"  {shape_id} | {shape_name} | diag={diag:.0f} | r={radius:.0f}")
            print("-" * 65)

            for algo_name in algo_names:
                done += 1
                progress = f"[{done:3d}/{total}]"
                print(f"  {progress} {algo_name:<25}", end='', flush=True)

                t_wall = time.perf_counter()
                n, elapsed, cov, dnf = run_one(algo_name, polygon, radius)
                wall = time.perf_counter() - t_wall

                if dnf:
                    tag = 'DNF'
                    print(f"  TIMEOUT ({wall:.1f}s)")
                else:
                    tag = 'OK'
                    print(f"  OK  {n:3d} circles  {elapsed:6.2f}s  cov={cov:.1f}%")

                writer.writerow({
                    'shape_id':     shape_id,
                    'shape_name':   shape_name,
                    'algorithm':    algo_name,
                    'n_circles':    n if not dnf else 'DNF',
                    'coverage_pct': f'{cov:.2f}' if not dnf else 'DNF',
                    'time_s':       f'{elapsed:.3f}',
                    'status':       tag,
                })
                f.flush()

    print("\n" + "=" * 65)
    print(f"  Done! Results saved to: {csv_path}")
    print("=" * 65 + "\n")


if __name__ == '__main__':
    multiprocessing.freeze_support()  # required on Windows
    main()
