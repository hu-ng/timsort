# Took inspiration from Tim Peter's original explanation,
# https://github.com/python/cpython/blob/master/Objects/listsort.txt

import random
import bisect


def reverse(lst, s, e):
    """Reverse the order of a list in place
    Input: s = starting index, e = ending index"""
    while s < e and s != e:
        lst[s], lst[e] = lst[e], lst[s]
        s += 1
        e -= 1


def make_temp_array(lst, s, e):
    """From the lst given, make a copy from index s to index e"""
    array = []
    while s <= e:
        array.append(lst[s])
        s += 1
    return array


def merge_compute_minrun(n):
    """Returns the minimum length of a run from 23 - 64 so that
    the len(array)/minrun is less than or equal to a power of 2."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def count_run(lst, s_run):
    """Count the length of one run, returns starting/ending indices,
    a boolean value to present increasing/decreasing run,
    and the length of the run"""
    increasing = True

    # If count_run started at the final position of the array
    if s_run == len(lst) - 1:
        return [s_run, s_run, increasing, 1]
    else:
        e_run = s_run
        # Decreasing run (strictly decreasing):
        if lst[s_run] > lst[s_run + 1]:
            while lst[e_run] > lst[e_run + 1]:
                e_run += 1
                if e_run == len(lst) - 1:
                    break
            increasing = False
            return [s_run, e_run, increasing, e_run - s_run + 1]

        # Increasing run (non-decreasing):
        else:
            while lst[e_run] <= lst[e_run + 1]:
                e_run += 1
                if e_run == len(lst) - 1:
                    break
            return [s_run, e_run, increasing, e_run - s_run + 1]


def bin_sort(lst, s, e, extend):
    """Binary insertion sort, assumed that lst[s:e + 1] is sorted.
    Extend the run by the number indicated by 'extend'"""

    for i in range(1, extend + 1):
        pos = 0
        start = s
        end = e + i

        # Value to be inserted
        value = lst[end]

        # If the value is already bigger than the last element from start -> end:
        # Don't do the following steps
        if value >= lst[end - 1]:
            continue

        # While-loop does the binary search
        while start <= end:
            if start == end:
                if lst[start] > value:
                    pos = start
                    break
                else:
                    pos = start + 1
                    break
            mid = (start + end) // 2
            if value >= lst[mid]:
                start = mid + 1
            else:
                end = mid - 1

        if start > end:
            pos = start

        # 'Push' the elements to the right by 1 element
        # Copy the value back the right position.
        for x in range(e + i, pos, - 1):
            lst[x] = lst[x - 1]
        lst[pos] = value


def gallop(lst, val, low, high, ltr):
    """Find the index of val in the slice[low:high]"""

    if ltr == True:
        # Used for merging from left to right
        # The index found will be so that every element prior
        # to that index is strictly smaller than val
        pos = bisect.bisect_left(lst, val, low, high)
        return pos

    else:
        # Used for merging from right to left
        # The index found will be so that every element from
        # that index onwards is strictly larger than val
        pos = bisect.bisect_right(lst, val, low, high)
        return pos


def merge(lst, stack, run_num):
    """Merge the two runs and update the remaining runs in the stack
    Only consequent runs are merged, one lower, one upper."""

    # Make references to the to-be-merged runs
    run_a = stack[run_num]
    run_b = stack[run_num + 1]

    # Make a reference to where the new combined run would be.
    new_run = [run_a[0], run_b[1], True, run_b[1] - run_a[0] + 1]

    # Put this new reference in the correct position in the stack
    stack[run_num] = new_run

    # Delete the upper run of the two runs from the stack
    del stack[run_num + 1]

    # If the length of run_a is smaller than or equal to length of run_b
    if run_a[3] <= run_b[3]:
        merge_low(lst, run_a, run_b, 7)

    # If the length of run_a is bigger than length of run_b
    else:
        merge_high(lst, run_a, run_b, 7)


def merge_low(lst, a, b, min_gallop):
    """Merges the two runs quasi in-place if a is the smaller run
    - a and b are lists that store data of runs
    - min_gallop: threshold needed to switch to galloping mode
    - galloping mode: uses gallop() to 'skip' elements instead of linear merge"""

    # Make a copy of the run a, the smaller run
    temp_array = make_temp_array(lst, a[0], a[1])
    # The first index of the merging area
    k = a[0]
    # Counter for the temp array of a
    i = 0
    # Counter for b, starts at the beginning
    j = b[0]

    gallop_thresh = min_gallop
    while True:
        a_count = 0  # number of times a win in a row
        b_count = 0  # number of times b win in a row

        # Linear merge mode, taking note of how many times a and b wins in a row.
        # If a_count or b_count > threshold, switch to gallop
        while i <= len(temp_array) - 1 and j <= b[1]:

            # if elem in a is smaller, a wins
            if temp_array[i] <= lst[j]:
                lst[k] = temp_array[i]
                k += 1
                i += 1

                a_count += 1
                b_count = 0

                # If a runs out during linear merge
                # Copy the rest of b
                if i > len(temp_array) - 1:
                    while j <= b[1]:
                        lst[k] = lst[j]
                        k += 1
                        j += 1
                    return

                # threshold reached, switch to gallop
                if a_count >= gallop_thresh:
                    break

            # if elem in b is smaller, b wins
            else:
                lst[k] = lst[j]
                k += 1
                j += 1

                a_count = 0
                b_count += 1

                # If b runs out during linear merge
                # copy the rest of a
                if j > b[1]:
                    while i <= len(temp_array) - 1:
                        lst[k] = temp_array[i]
                        k += 1
                        i += 1
                    return

                # threshold reached, switch to gallop
                if b_count >= gallop_thresh:
                    break

        # If one run is winning consistently, switch to galloping mode.
        # i, j, and k are incremented accordingly
        while True:
            # Look for the position of b[j] in a
            # bisect_left() -> a_adv = index in the slice [i: len(temp_array)]
            # so that every elem before temp_array[a_adv] is strictly smaller than lst[j]
            a_adv = gallop(temp_array, lst[j], i, len(temp_array), True)

            # Copy the elements prior to a_adv to the merge area, increment k
            for x in range(i, a_adv):
                lst[k] = temp_array[x]
                k += 1

            # Update the a_count to check successfulness of galloping
            a_count = a_adv - i

            # Advance i to a_adv
            i = a_adv

            # If run a runs out
            if i > len(temp_array) - 1:
                # Copy all of b over, if there is any left
                while j <= b[1]:
                    lst[k] = lst[j]
                    k += 1
                    j += 1
                return

            # Copy b[j] over
            lst[k] = lst[j]
            k += 1
            j += 1

            # If b runs out
            if j > b[1]:
                # Copy all of a over, if there is any left
                while i < len(temp_array):
                    lst[k] = temp_array[i]
                    k += 1
                    i += 1
                return

            # ------------------------------------------------------

            # Look for the position of a[i] in b
            # b_adv is analogous to a_adv
            b_adv = gallop(lst, temp_array[i], j, b[1] + 1, True)
            for y in range(j, b_adv):
                lst[k] = lst[y]
                k += 1

            # Update the counters and check the conditions
            b_count = b_adv - j
            j = b_adv

            # If b runs out
            if j > b[1]:
                # copy the rest of a over
                while i <= len(temp_array) - 1:
                    lst[k] = temp_array[i]
                    k += 1
                    i += 1
                return

            # copy a[i] over to the merge area
            lst[k] = temp_array[i]
            i += 1
            k += 1

            # If a runs out
            if i > len(temp_array) - 1:
                # copy the rest of b over
                while j <= b[1]:
                    lst[k] = lst[j]
                    k += 1
                    j += 1
                return

            # if galloping proves to be unsuccessful, return to linear
            if a_count < gallop_thresh and b_count < gallop_thresh:
                break

        # punishment for leaving galloping
        # makes it harder to enter galloping next time
        gallop_thresh += 1


def merge_high(lst, a, b, min_gallop):
    """Merges the two runs quasi in-place if b is the smaller run
    - Analogous to merge_low, but starts from the end
    - a and b are lists that store data of runs
    - min_gallop: threshold needed to switch to galloping mode
    - galloping mode: uses gallop() to 'skip' elements instead of linear merge"""

    # Make a copy of b, the smaller run
    temp_array = make_temp_array(lst, b[0], b[1])

    # Counter for the merge area, starts at the last index of array b
    k = b[1]
    # Counter for the temp array

    i = len(temp_array) - 1  # Lower bound is 0

    # Counter for a, starts at the end this time
    j = a[1]

    gallop_thresh = min_gallop
    while True:
        a_count = 0  # number of times a win in a row
        b_count = 0  # number of times b win in a row

        # Linear merge, taking note of how many times a and b wins in a row.
        # If a_count or b_count > threshold, switch to gallop
        while i >= 0 and j >= a[0]:
            if temp_array[i] > lst[j]:
                lst[k] = temp_array[i]
                k -= 1
                i -= 1

                a_count = 0
                b_count += 1

                # If b runs out during linear merge
                if i < 0:
                    while j >= a[0]:
                        lst[k] = lst[j]
                        k -= 1
                        j -= 1
                    return

                if b_count >= gallop_thresh:
                    break

            else:
                lst[k] = lst[j]
                k -= 1
                j -= 1

                a_count += 1
                b_count = 0

                # If a runs out during linear merge
                if j < a[0]:
                    while i >= 0:
                        lst[k] = temp_array[i]
                        k -= 1
                        i -= 1
                    return

                if a_count >= gallop_thresh:
                    break

        # i, j, k are DECREMENTED in this case
        while True:
            # Look for the position of b[i] in a[0, j + 1]
            # ltr = False -> uses bisect_right()
            a_adv = gallop(lst, temp_array[i], a[0], j + 1, False)

            # Copy the elements from a_adv -> j to merge area
            # Go backwards to the index a_adv
            for x in range(j, a_adv - 1, -1):
                lst[k] = lst[x]
                k -= 1

            # # Update the a_count to check successfulness of galloping
            a_count = j - a_adv + 1

            # Decrement index j
            j = a_adv - 1

            # If run a runs out:
            if j < a[0]:
                while i >= 0:
                    lst[k] = temp_array[i]
                    k -= 1
                    i -= 1
                return

            # Copy the b[i] into the merge area
            lst[k] = temp_array[i]
            k -= 1
            i -= 1

            # If a runs out:
            if i < 0:
                while j >= a[0]:
                    lst[k] = lst[j]
                    k -= 1
                    j -= 1
                return

            # -------------------------------------------------

            # Look for the position of A[j] in B:
            b_adv = gallop(temp_array, lst[j], 0, i + 1, False)
            for y in range(i, b_adv - 1, -1):
                lst[k] = temp_array[y]
                k -= 1

            b_count = i - b_adv + 1
            i = b_adv - 1

            # If b runs out:
            if i < 0:
                while j >= a[0]:
                    lst[k] = lst[j]
                    k -= 1
                    j -= 1
                return

            # Copy the a[j] back to the merge area
            lst[k] = lst[j]
            k -= 1
            j -= 1

            # If a runs out:
            if j < a[0]:
                while i >= 0:
                    lst[k] = temp_array[i]
                    k -= 1
                    i -= 1
                return

            # if galloping proves to be unsuccessful, return to linear
            if a_count < gallop_thresh and b_count < gallop_thresh:
                break

        # punishment for leaving galloping
        gallop_thresh += 1


def merge_collapse(lst, stack):
    """The last three runs in the stack is A, B, C.
    Maintains invariants so that their lengths: A > B + C, B > C
    Translated to stack positions:
       stack[-3] > stack[-2] + stack[-1]
       stack[-2] > stack[-1]
    Takes a stack that holds many lists of type [s, e, bool, length]"""

    # This loops keeps running until stack has one element
    # or the invariant holds.
    while len(stack) > 1:
        if len(stack) >= 3 and stack[-3][3] <= stack[-2][3] + stack[-1][3]:
            if stack[-3][3] < stack[-1][3]:
                # merge -3 and -2, merge at -3
                merge(lst, stack, -3)
            else:
                # merge -2 and -1, merge at -2
                merge(lst, stack, -2)
        elif stack[-2][3] <= stack[-1][3]:
            # merge -2 and -1, merge at -2
            merge(lst, stack, -2)
        else:
            break


def merge_force_collapse(lst, stack):
    """When the invariant holds and there are > 1 run
    in the stack, this function finishes the merging"""
    while len(stack) > 1:
        # Only merges at -2, because when the invariant holds,
        # merging would be balanced
        merge(lst, stack, -2)


def timsort(lst):
    """The main function"""

    # Starting index
    s = 0

    # Ending index
    e = len(lst) - 1

    # The stack
    stack = []

    # Compute min_run using size of lst
    min_run = merge_compute_minrun(len(lst))

    while s <= e:

        # Find a run, return [start, end, bool, length]
        run = count_run(lst, s)

        # If decreasing, reverse
        if run[2] == False:
            reverse(lst, run[0], run[1])
            # Change bool to True
            run[2] = True

        # If length of the run is less than min_run
        if run[3] < min_run:
            # The number of indices by which we want to extend the run
            # either by the distance to the end of the lst
            # or by the length difference between run and minrun
            extend = min(min_run - run[3], e - run[1])

            # Extend the run using binary insertion sort
            bin_sort(lst, run[0], run[1], extend)

            # Update last index of the run
            run[1] = run[1] + extend

            # Update the run length
            run[3] = run[3] + extend

        # Push the run into the stack
        stack.append(run)

        # Start merging to maintain the invariant
        merge_collapse(lst, stack)

        # Update starting position to find the next run
        # If run[1] == end of the lst, s > e, loop exits
        s = run[1] + 1

    # Some runs might be left in the stack, complete the merging.
    merge_force_collapse(lst, stack)

    # Return the lst, ta-da.
    return lst
