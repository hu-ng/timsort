# Code for traditional merge sort, implemented using pseudo code from Cormen et al.
def mergesort(A, p, r):
    if p < r:
        q = (p + r)//2
        mergesort(A, p, q)
        mergesort(A, q + 1, r)
        merge_helper(A, p, q, r)


def merge_helper(A, p, q, r):
    n1 = q - p + 1
    n2 = r - q
    L = [None]*(n1 + 1)
    R = [None]*(n2 + 1)
    for i in range(n1):
        L[i] = A[p + i]
    for j in range(n2):
        R[j] = A[q + 1 + j]
    L[n1] = float('inf')
    R[n2] = float('inf')
    i = 0
    j = 0
    for k in range(p, r + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1
