# Copyright © 2020 way2FAANG
# LeetCode: 632

from heapq import heappush, heappop

# m lists, n elements per list - Worst case
# Time(nm*log(m)) | Space: O(m)
# Brute force would have been O(nm*log(nm))
def find_smallest_range(lists):
    range_start, range_end = -float('inf'), float('inf')
    current_max_num = -float('inf')

    min_heap = []
    for i, list_ in enumerate(lists):
        heappush(min_heap, (list_[0], i, 0))
        current_max_num = max(current_max_num, list_[0])

    while len(min_heap) == len(lists):
        smallest_num, list_index, num_index_in_list = heappop(min_heap)
        # update range if current smallest num and max num give smaller range
        if current_max_num - smallest_num < range_end - range_start:
            range_start = smallest_num
            range_end = current_max_num

        # insert next num of that list in the heap
        # update current max ( we are updating current max during insertion in heap)
        if num_index_in_list + 1 < len(lists[list_index]):
            num_to_insert = lists[list_index][num_index_in_list + 1]
            heappush(min_heap, (num_to_insert, list_index, num_index_in_list + 1))
            current_max_num = max(current_max_num, num_to_insert)

    return [range_start, range_end]

def main():
    print("Smallest range is: " +
          str(find_smallest_range([[1, 5, 8], [4, 12], [7, 8, 10]])))


main()
