# Copyright © 2020 way2FAANG
# LeetCode: 378

from heapq import heappush, heappop


# Time : O(min(k,n) + k*log(min(n,k)))
# - similar logic to previous prob. min comes in because we are using the fact cols are sorted in case when k < n
# | Space: O(n) - for heap
def find_Kth_smallest(matrix, k):
    smallest_nums_visited = 0
    min_heap = []
    n = len(matrix)
    # given - square matrix
    # we will be considering the matrix as list of lists (rows)
    # we can apply one optimization here - consider min of k and n
    # why can we do that ? because even cols are sorted
    # so in case k < n, the 0th element of first k rows will be the min
    for i in range(min(k, n)):
        heappush(min_heap, (matrix[i][0], i, 0))  # element belonging to 0th col in rth row

    while min_heap and smallest_nums_visited < k:
        smallest_num, r, c = heappop(min_heap)
        smallest_nums_visited += 1
        if c + 1 < n:
            heappush(min_heap, (matrix[r][c + 1], r, c + 1))

    return smallest_num


def main():
    print("Kth smallest number is: " +
          str(find_Kth_smallest([[2, 6, 8], [3, 7, 10], [5, 8, 11]], 5)))


main()
