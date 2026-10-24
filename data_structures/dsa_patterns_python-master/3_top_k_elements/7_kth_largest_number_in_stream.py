# Copyright © 2020 way2FAANG
# LeetCode: 703


from heapq import heappush, heappop

class KthLargestNumberInStream:
    # Time: O(n*log(k)) | Space (O(k))
    # As opposed to keeping nums and sorting - Time: O(n* log(n)) | Space: O(n)
    def __init__(self, nums, k):
        self.min_heap = []
        for num in nums:
            heappush(self.min_heap, num)
            if len(self.min_heap) > k:
                heappop(self.min_heap)
        self.k = k

    # Time: O(log(k))
    # As opposed to insertion sort: Time: O(n)
    def add(self, num):
        heappush(self.min_heap, num)
        heappop(self.min_heap)
        return self.min_heap[0]


def main():
    kthLargestNumber = KthLargestNumberInStream([3, 1, 5, 12, 2, 11], 4)
    print("4th largest number is: " + str(kthLargestNumber.add(6)))
    print("4th largest number is: " + str(kthLargestNumber.add(13)))
    print("4th largest number is: " + str(kthLargestNumber.add(4)))


main()
