# Copyright © 2020 way2FAANG
# LeetCode: 658


from heapq import heappush, heappop


# Time: O(n*log(k)) | Space: O(k)
def find_closest_elements(arr, K, X):
    max_heap = []

    for num in arr:
        dist_from_X = abs(num - X)
        heappush(max_heap, (-dist_from_X, num))
        if len(max_heap) > K:
            heappop(max_heap)

    return sorted([num for _, num in max_heap])


# O(log(N) + klog(k)) - better
def find_closest_elements(arr, K, X):
    max_heap = []
    # find index of closest element to X
    index = binary_search(arr, X)
    low, high = index-K, index+K

    # low cannot go below 0
    low = max(0, low)

    # high cannot go above len(arr)-1
    high = min(high, len(arr)-1)

    # push k elements either side into the heap
    for i in range(low, high+1):
        dist = abs(arr[i] - X)
        heappush(max_heap, (-dist, arr[i]))
        if len(max_heap) > K:
            heappop(max_heap)  # to maintain k closest elements
    result = sorted(num for dist, num in max_heap)

    return result


def binary_search(arr, key):
    # iterative, find closest match
    start, end = 0, len(arr) - 1
    while start <= end:
        mid = (start + end) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] >= key:
            end = mid - 1
        else:
            start = mid + 1
    return mid


def main():
    print("'K' closest numbers to 'X' are: " +
          str(find_closest_elements([5, 6, 7, 8, 9], 3, 7)))
    print("'K' closest numbers to 'X' are: " +
          str(find_closest_elements([2, 4, 5, 6, 9], 3, 6)))
    print("'K' closest numbers to 'X' are: " +
          str(find_closest_elements([2, 4, 5, 6, 9], 3, 10)))


main()
