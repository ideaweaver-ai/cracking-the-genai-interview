# Copyright © 2020 way2FAANG


from heapq import heappush, heappop, heapify

# Using min heap
# # Time = O(n) + O(k1*log(n) + O(k2*log(n)) | Space: O(n)
# def find_sum_of_elements(nums, k1, k2):
#     # input validation
#     if k1 > k2:
#         return 0
#
#     result = 0
#
#     # O(n)
#     heapify(nums)
#
#     # O( k1 * log(n))
#     for _ in range(k1):
#         if nums:
#             heappop(nums)
#
#     # O( (k2-k1) * log(n-k1) )
#     for _ in range(k2 - k1 - 1):
#         if nums:
#             result += heappop(nums)
#
#     return result


# Better solution
# O(n*log(k2)) + O(k2*log(k2)) = O(n*log(k2)) | Space: O(k2)
def find_sum_of_elements(nums, k1, k2):
    max_heap = []
    # Collect k2-1 smallest elements in the array - since k2th element not included in sum
    for num in nums:
        heappush(max_heap, -num)

        if len(max_heap) > k2 - 1:
            heappop(max_heap)

    # add the top k2-k1-1 max elements from the heap
    total_sum = 0
    for i in range(k2 - k1 - 1):
        total_sum += -heappop(max_heap)

    return total_sum


def main():
    print("Sum of all numbers between k1 and k2 smallest numbers: " +
          str(find_sum_of_elements([1, 3, 12, 5, 15, 11], 3, 6)))
    print("Sum of all numbers between k1 and k2 smallest numbers: " +
          str(find_sum_of_elements([3, 5, 8, 7], 1, 4)))


main()
