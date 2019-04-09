from timsort import timsort
import random

# Emtpy array
lst1 = []
# Single element
lst2 = [1]
# Two elements
lst3 = [1, 2]
# Alternating elements
lst4 = [-1,2] * 1000
# Ordered elements with pos and neg values
lst5 = [i for i in range(-1000, 1000)]
# Inversely ordered elements with pos and neg values
lst6 = [i for i in range(1000, -1000, -1)]
# Even number of random ints
lst7 = [random.randint(-10000, 10000) for i in range(1000)]
# Odd number of random ints
lst8 = [random.randint(-10000, 10000) for i in range(999)]
# More alternating elements
lst9 = [-1,2,-3,4,5]*1000
# Floats
lst10 = [(i + 0.2) for i in range(10000)]
# Ordered even numbers
lst11 = [i for i in range(1000, 2)]
# Full of zeros
lst12 = [0 for i in range(1000)]
# Inversely ordered odd numbers
lst13 = [i for i in range(9999, -1, -2)]

test_cases = [lst1, lst2, lst3, lst4, lst5, lst6, lst7,
              lst8, lst9, lst10, lst11, lst12, lst13]

test_cases_alt = [lst1, lst2, lst3, lst4, lst5, lst6, lst7,
              lst8, lst9, lst10, lst11, lst12, lst13]

def test_sort():
    """Test accuracy of algorithm"""
    for lst in test_cases:
        # Make a copy of the case
        sortable = lst.copy()

        # Make another copy of the case
        sortable_copy = lst.copy()
        sorted_copy = timsort(sortable_copy)

        assert sorted_copy is sortable_copy
        assert sorted_copy == sorted(sortable)

    return "No error"


def test_sort_alt():
    for lst in test_cases_alt:
        # Create a copy of the list
        copy = lst.copy()

        timsort(lst)
        # Compare each element to the next element
        for i in range(len(lst) - 1):
            assert lst[i] <= lst[i + 1]

        # Assure that the lengths are the same
        assert len(copy) == len(lst)

        # Sort the copy using default
        copy.sort()

        # Every element in lst is in copy
        for i in range(len(lst)):
            assert copy[i] == lst[i]

    return 'No error'

test_sort_alt(), test_sort()
