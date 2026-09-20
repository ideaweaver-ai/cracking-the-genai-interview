# Copyright © 2020 way2FAANG
# LeetCode: 347


from heapq import heappush, heappop


# Time O(n) + O(n*log(k)) [if k > 2 Time = O(n*log(k), if k <= 2 -> O(n)] | Space: O(n)
def find_k_frequent_numbers(nums, k):
    # naming of variables is important
    num_freq_map = {}
    # heap should be reverse of what is required
    # for largest elements -> min heap, for smallest elements -> max heap
    # for this problem we use min heap since we require k most frequent elements
    # the heap maintains the k most frequent elements in the arr at any point of time
    min_heap = []

    # since we need most frequent items, create a frequency map of nums
    for num in nums:
        # so it doesn't give key error. can use defaultdict(int)
        num_freq_map[num] = num_freq_map.get(num, 0) + 1

    for num, freq in num_freq_map.items():
        # we want to track numbers in min_heap based on the frequency
        # in such a case when the item is different from the metric to track in heap
        # we can use tuple (metric, item) - min heap will perform operations based on metric
        heappush(min_heap, (freq, num))
        # we want to store only k largest/ smallest elements
        # so, ensure heap len is always k
        if len(min_heap) > k:
            heappop(min_heap)

    # return output - note minheap consists of top k nums and their frequencies
    return [num for freq, num in min_heap]


def main():
    print("Here are the K frequent numbers: " +
          str(find_k_frequent_numbers([1, 3, 5, 12, 11, 12, 11], 2)))

    print("Here are the K frequent numbers: " +
          str(find_k_frequent_numbers([5, 12, 11, 3, 11], 2)))


main()
