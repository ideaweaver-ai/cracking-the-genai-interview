# This is not a Leetcode problem. This problem is just to warm you up to this patttern
# Problem:
# Given an array of integers and a positve integer k, find the average of all subarrays of size k. The result should be an array/list

# Brute force
# O(N*K) time | O(1) space
# def find_averages_of_subarrays(arr, K):
#     result = []
#     for i in range(len(arr) - K + 1):
#         # find sum of next 'K' elements
#         sum_ = 0.0
#         for j in range(i, i + K):
#             sum_ += arr[j]
#         result.append(sum_ / K)  # calculate average
#     return result


# O(N) time | O(1) space
def find_averages_of_subarrays(arr, K):
    # initialize output
    result = []
    # define window start and window metric
    start, sum_ = 0, 0.0
    for end in range(len(arr)):
        # expand window
        sum_ += arr[end]  # add current element to window
        # validate window
        if end >= K - 1:
            # update result
            result.append(sum_ / K)
            # shrink window
            sum_ -= arr[start]
            start += 1
    # return result
    return result


def main():
    result = find_averages_of_subarrays([1, 2, 3, 4, 5], 3)
    print("Averages of subarrays of size K: " + str(result))
    result = find_averages_of_subarrays([1, 3, 2, 6, -1, 4, 1, 8, 2], 5)
    print("Averages of subarrays of size K: " + str(result))


main()
