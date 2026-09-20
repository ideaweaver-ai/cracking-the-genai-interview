# Copyright © 2020 way2FAANG


from heapq import *


# def find_k_largest_numbers(nums, k):
#     result = []
#     for i in range(k):
#         heappush(result, nums[i])
#     for num in nums[k:]:
#         if num > result[0]:
#             heappop(result)
#             heappush(result, num)
#     # TODO: Write your code here
#     return list(result)


# Time: O(n * log(k)) | Space: O(k)
# We will follow this format - much cleaner code
def find_k_largest_numbers(nums, k):
    # heap should be reverse of what is required
    # for largest elements -> min heap, for smallest elements -> max heap
    # for this problem we use min heap since we require k largest elements
    # the heap maintains the k largest elements in the arr at any point of time
    min_heap = []
    for num in nums:
        heappush(min_heap, num)
        # we want to store only k largest/ smallest elements
        # so, ensure heap len is always k
        if len(min_heap) > k:
            heappop(min_heap)

    return min_heap


def main():
    print("Here are the top K numbers: " +
          str(find_k_largest_numbers([3, 1, 5, 12, 2, 11], 3)))

    print("Here are the top K numbers: " +
          str(find_k_largest_numbers([5, 12, 11, -1, 12], 3)))


main()
