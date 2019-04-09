from timsort import timsort
from normal_merge import mergesort

import matplotlib.pyplot as plt
import time
import math

# With random data
def graph_runtimes(length_lst, repeats):
    merge_avg = []
    timsort_avg = []
    theory_time = [0]

    # Providing data for theoretical run times
    # Adjusted so it matches the curve created by the algorithms
    for i in range(1, length_lst):
        theory_time.append(i*math.log(i)/1100000)

    # Nested for loop: for every length N, run algorithms 'repeats' times
    # Average the results, append into lists
    for i in range(length_lst):
        merge_lst = []
        timsort_lst = []

        for x in range(repeats):
            mylist = random.sample(range(i), i)
            copy = mylist.copy()

            start_time = time.time()
            mergesort(mylist, 0, len(mylist) - 1)
            finish_time = time.time() - start_time
            merge_lst.append(finish_time)

            start_time = time.time()
            timsort(copy)
            finish_time = time.time() - start_time
            timsort_lst.append(finish_time)

        avg_merge = sum(merge_lst)/len(merge_lst)
        avg_timsort = sum(timsort_lst)/len(timsort_lst)

        merge_avg.append(avg_merge)
        timsort_avg.append(avg_timsort)

    # Plot individual graphs for each curve
    plt.plot(merge_avg, color='red', label = 'Traditional merge')
    plt.plot(timsort_avg, color='blue', label = 'TimSort')
    plt.plot(theory_time, color='green', label = 'Theoretical run time O(nlog(n))')
    plt.xlabel("Length of the list")
    plt.ylabel("Averaged run-time")
    plt.legend()
    plt.show()


# With worst case traditional merge sort - maximum comparisons:
def worstCases(n):
    """Generates the worst case scenario for merge sort
    with maxiimum comparisons possible for every size N"""

    # Holds base cases of N = 1, N = 2
    lst = [[], [1], [2,1]]

    # Builds worst cases from the bottom up
    for i in range(3, n + 1):
        left = lst[i//2]
        right = lst[i - i//2]
        left = [x*2 for x in left]
        right = [y*2 - 1 for y in right]
        entry = left + right
        lst.append(entry)
    return lst


def graph_runtimes_worst(length_lst, repeats):
    merge_avg = []
    timsort_avg = []
    theory_time = [0]
    worst_cases = worstCases(length_lst)

    for i in range(1, length_lst):
        theory_time.append(i*math.log(i)/1000000)

    for i in worst_cases:
        merge_lst = []
        timsort_lst = []

        for x in range(repeats):
            mylist = i
            copy = mylist.copy()

            start_time = time.time()
            mergesort(mylist, 0, len(mylist) - 1)
            finish_time = time.time() - start_time
            merge_lst.append(finish_time)

            start_time = time.time()
            timsort(copy)
            finish_time = time.time() - start_time
            timsort_lst.append(finish_time)

        avg_merge = sum(merge_lst)/len(merge_lst)
        avg_timsort = sum(timsort_lst)/len(timsort_lst)

        merge_avg.append(avg_merge)
        timsort_avg.append(avg_timsort)

    plt.plot(merge_avg, color='red', label = 'Traditional merge')
    plt.plot(timsort_avg, color='blue', label = 'TimSort')
    plt.plot(theory_time, color='green', label = 'Theoretical run time O(nlog(n))')
    plt.xlabel("Length of the list")
    plt.ylabel("Averaged run-time")
    plt.legend()
    plt.show()


# With sorted data - best case Timsort:
def graph_runtimes_best(length_lst, repeats):
    """Identical to graph_runtimes, but with ordered data"""
    merge_avg = []
    timsort_avg = []
    theory_time = [0]

    for i in range(1, length_lst):
        theory_time.append(i*math.log(i)/1000000)

    for i in range(length_lst):
        merge_lst = []
        timsort_lst = []

        for x in range(repeats):

            # Here is the only change
            mylist = [x for x in range(i)]
            copy = mylist.copy()

            start_time = time.time()
            mergesort(mylist, 0, len(mylist) - 1)
            finish_time = time.time() - start_time
            merge_lst.append(finish_time)

            start_time = time.time()
            timsort(copy)
            finish_time = time.time() - start_time
            timsort_lst.append(finish_time)

        avg_merge = sum(merge_lst)/len(merge_lst)
        avg_timsort = sum(timsort_lst)/len(timsort_lst)

        merge_avg.append(avg_merge)
        timsort_avg.append(avg_timsort)

    plt.plot(merge_avg, color='red', label = 'Traditional merge')
    plt.plot(timsort_avg, color='blue', label = 'TimSort')
    plt.plot(theory_time, color='green', label = 'Theoretical run time O(nlog(n))')
    plt.xlabel("Length of the list")
    plt.ylabel("Averaged run-time")
    plt.legend()
    plt.show()

graph_runtimes_best(500, 200)
