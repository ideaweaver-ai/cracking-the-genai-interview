# Copyright © 2020 way2FAANG
# LeetCode: 215


from heapq import heappush, heappop


# def find_Kth_smallest_number(nums, k):
#     # TODO: Write your code here
#     max_heap = []
#     for i in range(k):
#         heappush(max_heap, -nums[i])
#     for i in range(k, len(nums)):
#         if nums[i] < -max_heap[0]:
#             heappop(max_heap)
#             heappush(max_heap, -nums[i])
#     return -max_heap[0]


# Time: O(n*log(k)) | Space: O(k)
def find_Kth_smallest_number(nums, k):
    # heap should be reverse of what is required
    # for largest elements -> min heap, for smallest elements -> max heap
    # for this problem we use max heap since we require k smallest elements
    # the heap maintains the k smallest elements in the arr at any point of time
    max_heap = []
    for num in nums:
        # imp - python has only min heap
        # to get functionality of max heap we simply push -ive of num in the min heap
        heappush(max_heap, -num)
        # we want to store only k largest/ smallest elements
        # so, ensure heap len is always k
        if len(max_heap) > k:
            heappop(max_heap)
        # imp - why -ive ? remember we pushed -ive num, as we wanted a max heap
    return -max_heap[0]


# Alternative approach using min heap
# Time: O(n) + O(k*log(n))
# def find_Kth_smallest_number(nums, k):
#     # Push all n elements into the min heap
#     # Pop k elements to return the kth smallest element
#     min_heap = []
#     for num in nums:
#         heappush(min_heap, num)
#
#     result = None
#     for _ in range(k):
#         result = heappop(min_heap)
#
#     return result


def main():
    print("Kth smallest number is: " +
          str(find_Kth_smallest_number([1, 5, 12, 2, 11, 5], 3)))

    # since there are two 5s in the input array, our 3rd and 4th smallest numbers should be a '5'
    print("Kth smallest number is: " +
          str(find_Kth_smallest_number([1, 5, 12, 2, 11, 5], 4)))

    print("Kth smallest number is: " +
          str(find_Kth_smallest_number([5, 12, 11, -1, 12], 3)))


main()
