# Copyright © 2020 way2FAANG
# LeetCode: 702

import math


class ArrayReader:

    def __init__(self, arr):
        self.arr = arr

    def get(self, index):
        if index >= len(self.arr):
            return math.inf
        return self.arr[index]


# Time: O(log(n)) | Space: O(1)
def search_in_infinite_array(reader, key):
    def binary_search(start, end):
        while start <= end:
            mid = start + (end - start) // 2
            if key == reader.get(mid):
                return mid
            elif key < reader.get(mid):
                end = mid - 1
            else:
                start = mid + 1
        return -1

    # main function
    # try to figure range for binary search by doubling it every time - this maintains O(log(n)) time
    start, end, size = 0, 0, 1
    while key > reader.get(end):
        # while end is less than key double the range
        start = end+1  # using another var because we will use start in next eq to double range
        size = 2*size
        end = start+size-1

    return binary_search(start, end)


def main():
    reader = ArrayReader([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30])
    print(search_in_infinite_array(reader, 16))
    print(search_in_infinite_array(reader, 11))
    reader = ArrayReader([1, 3, 8, 10, 15])
    print(search_in_infinite_array(reader, 15))
    print(search_in_infinite_array(reader, 200))


main()







