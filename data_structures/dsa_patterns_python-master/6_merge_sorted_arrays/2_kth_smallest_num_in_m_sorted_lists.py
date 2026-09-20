from heapq import heappush, heappop


# find the minimum number from all lists current min (since they are sorted) using min heap
# if it is the kth number return
# else insert the next number from that list in the min heap
# So what do we need to inseert in the heap?
# current num, list number, index of current element

# Time: O(k*log(m) - 'm' is num of lists | Space: O(m)
# since we have to pop only k nums from heap sized m
def find_Kth_smallest(lists, k):
    smallest_nums_visited = 0
    min_heap = []
    # 1 Add smallest element of each list(array) to heap
    for i, list_ in enumerate(lists):
        if list_:
            heappush(min_heap, (list_[0], i, 0))  # since we need the list whose element was popped from min heap

    # 2 keep on getting the next min amongst all lists(arrays)
    while min_heap and smallest_nums_visited < k:
        smallest_num, list_index, index_of_num_in_list = heappop(min_heap)
        smallest_nums_visited += 1
        list_to_insert = lists[list_index]
        # 3 check if current smallest num's list (array) has next element and insert it into heap
        if index_of_num_in_list + 1 < len(list_to_insert):
            heappush(min_heap, (list_to_insert[index_of_num_in_list + 1], list_index, index_of_num_in_list + 1))

    return smallest_num



def main():
    print("Kth smallest number is: " +
          str(find_Kth_smallest([[2, 6, 8], [3, 6, 7], [1, 3, 4]], 5)))

    print("Kth smallest number is: " +
          str(find_Kth_smallest([[5, 8, 9], [1, 7]], 3)))


main()
