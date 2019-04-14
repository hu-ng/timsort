# Timsort in Python !

## General instructions:
No dependencies are needed for to run the algorithm since it is all built in native Python. To get the module, do:

```
$ git clone https://github.com/hu-ng/timsort.git
```

To use, just import `timsort.py` and run `timsort()` as you would with the usual `sort()`!

## Description:
This was the Final Project for my Data Structure and Algorithms course, and I thought it would be a neat idea to apply algorithmic thinking and implement Timsort, the default sorting algorithm that Python uses, in native Python. Timsort is essentially mergesort but with many bells and whistles added for the sake of optimization, like the use of natural orderings of data and "galloping" - fast-forwarding through a list when a certain threshold is reached.

The project also includes a runtime comparison between my implementation of Timsort and traditional mergesort in the worst, average, and best cases, with accompanying graphs.
