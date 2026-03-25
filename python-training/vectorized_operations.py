import numpy as np
import time

# Generating anarray of 1 000 000 random integers
rand_arr = np.random.rand(1, 100, 1000000)

# Calculationg the sum of items in array
sum_arr = np.sum(rand_arr)

# Calculating standard deviation of items in array
std_dev_arr = np.std(rand_arr)

# Calculating mean of items in array
std_mean_arr = np.mean(rand_arr)


start_time = time.time()  # Capture start point
# Squaring each and substruct 0.5 from each item in array
result = (rand_arr**2) - 0.5

end_time = time.time()
duration = end_time - start_time  # Capture end point


def vectorized_operations():
    print(f"Sum of items in array: {sum_arr}")
    print(f"Standard deviation of items in array: {std_dev_arr}")
    print(f"Mean of items in array: {std_mean_arr}")
    print(f"Squared each item and subtracted 0.5 from each item in array: {result}")
    print(f"Execution time of 1 000 000 operations: {duration}")


if __name__ == "__main__":
    vectorized_operations()
