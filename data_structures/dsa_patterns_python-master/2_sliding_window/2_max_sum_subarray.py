
# This is not a Leetcode problem. This problem helps you to understand how to adjust the pattern as the problem changes.
# Compare how the window metric changes slightly from the previous problem

# Problem:
# Given an array of positive integers and a positve integer k, find the maximum sum amongst all subarrays of size k in the array. 
# The result should be an int

# Brute Force
# O(N*K) time | O(1) space
# def max_sub_array_of_size_k(arr, K):
#     max_sum = -float('inf')
#     for i in range(len(arr) - K + 1):
#         # find sum of next 'K' elements
#         win_sum = 0.0
#         for j in range(i, i + K):
#             win_sum += arr[j]
#         max_sum = max(max_sum, win_sum)
#     return max_sum


# O(N) time | O(1) space
def max_sub_array_of_size_k(arr, k):
    # initialize output
    max_sum = 0  # since positive nos array

    # define window start and window metric
    start, sum_ = 0, 0

    # slide window
    for end in range(len(arr)):
        # expand window
        sum_ += arr[end]  # add current element to window
        # validate window
        if end >= k - 1:
            # update result
            max_sum = max(max_sum, sum_)
            # shrink window
            sum_ -= arr[start]
            start += 1
    # return result
    return max_sum


def main():
    print("Maximum sum of a subarray of size K: " + str(max_sub_array_of_size_k([1, 2, 3, 4, 5], 3)))
    print("Maximum sum of a subarray of size K: " + str(max_sub_array_of_size_k([2, 1, 5, 1, 3, 2], 3)))
    print("Maximum sum of a subarray of size K: " + str(max_sub_array_of_size_k([2, 3, 4, 1, 5], 2)))


main()
