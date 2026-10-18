# Copyright © 2020 way2FAANG


from heapq import heappush, heappop


# We want to remove elements that have freq > 1 to make them distinct
# The element with min freq > 1 should be removed first as that gives the best chance to get a distinct element
# Time: O(n*log(n)+ k*log(n)) = O(n*log(n) | Space: O(n)
def find_maximum_distinct_elements(nums, k):
    # Create number frequency hashmap
    num_freq_map = {}
    for num in nums:
        num_freq_map[num] = num_freq_map.get(num, 0) + 1

    min_heap = []
    num_distinct_elements = 0

    # Store anything more than 1 frequency into the min heap, else it's already a distinct element
    for num, freq in num_freq_map.items():
        if freq == 1:
            num_distinct_elements += 1
        else:
            heappush(min_heap, (freq, num))

    while min_heap and k > 0:
        freq, num = heappop(min_heap)
        k -= freq - 1
        if k >= 0:
            num_distinct_elements += 1

    # We have removed all extra elements
    # if k is still remaining we need to remove distinct elements
    if k > 0:
        num_distinct_elements -= k

    return max(num_distinct_elements, 0)


def main():
    print("Maximum distinct numbers after removing K numbers: " +
          str(find_maximum_distinct_elements([7, 3, 5, 8, 5, 3, 3], 2)))
    print("Maximum distinct numbers after removing K numbers: " +
          str(find_maximum_distinct_elements([3, 5, 12, 11, 12], 3)))
    print("Maximum distinct numbers after removing K numbers: " +
          str(find_maximum_distinct_elements([1, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5], 2)))


main()
