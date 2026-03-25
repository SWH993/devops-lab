import numpy as np
import time


def compare_performance():
    # Setup: 1,000,000 random numbers
    size = 1000000
    rand_arr = np.random.rand(size)

    # --- METHOD 1: Traditional Python For Loop ---
    start_for = time.time()

    result_for = []
    for item in rand_arr:
        # Squaring and subtracting 0.5 manually
        val = (item**2) - 0.5
        result_for.append(val)

    end_for = time.time()
    for_duration = end_for - start_for

    # --- METHOD 2: NumPy Vectorized Operation ---
    start_numpy = time.time()

    # NumPy does this at the C-level (CPU instructions)
    result_numpy = (rand_arr**2) - 0.5

    end_numpy = time.time()
    numpy_duration = end_numpy - start_numpy

    # --- RESULTS ---
    print(f"--- Performance Benchmark ({size:,} elements) ---")
    print(f"Python For Loop: {for_duration:.6f} seconds")
    print(f"NumPy Vectorized: {numpy_duration:.6f} seconds")

    # Calculate how many times faster NumPy is
    multiplier = for_duration / numpy_duration
    print(f"\nResult: NumPy is {multiplier:.1f}x FASTER than a standard loop.")


if __name__ == "__main__":
    compare_performance()
