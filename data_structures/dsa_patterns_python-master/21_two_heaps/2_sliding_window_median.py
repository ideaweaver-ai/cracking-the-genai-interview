from heapq import heappush, heappop, heapify


class SlidingWindowMedian:

    def __init__(self):
        self.max_heap = []
        self.min_heap = []

    # Time: O(n*k) | Space: O(k)
    def find_sliding_window_median(self, nums, k):
        result = []
        start = 0

        for end in range(len(nums)):
            num = nums[end]
            # insert num in appropriate heap
            # O(log(k)
            if not self.max_heap or -self.max_heap[0] >= num:
                heappush(self.max_heap, -num)
            else:
                heappush(self.min_heap, num)

            self.rebalance()

            if end >= k - 1:
                result.append(self.calculate_median())
                self.remove(nums[start]) # O(k)
                start += 1

        return result

    # Time: O(k) | Space: O(1)
    # Time will be O(k) even if we find index, exchange with last element, delete it and then do _sift_up, _sift_down
    def remove(self, num):
        if -self.max_heap[0] >= num:
            self.max_heap.remove(-num)
            self.rebalance()
        else:
            self.min_heap.remove(num)
            self.rebalance()

    def calculate_median(self):
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2
        else:
            return -self.max_heap[0] / 1.0

    def rebalance(self):
        if len(self.max_heap) - len(self.min_heap) > 1:
            heappush(self.min_heap, -heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heappush(self.max_heap, -heappop(self.min_heap))


def main():
    slidingWindowMedian = SlidingWindowMedian()
    result = slidingWindowMedian.find_sliding_window_median(
        [1, 2, -1, 3, 5], 2)
    print("Sliding window medians are: " + str(result))
    result = slidingWindowMedian.find_sliding_window_median(
        [1, 2, -1, 3, 5], 3)
    print("Sliding window medians are: " + str(result))


if __name__ == "__main__":
    main()
