from typing import List
from heapq import heappush, heappop


class MedianOfAStream:
    def __init__(self):
        # design choice: max_heap to have the extra element when total elements are odd
        self.first_half = []  # max heap - have all elements <= median
        self.second_half = []  # min heap - have all elements > median

    # Time: O(log(n)) - improvement from O(n) inserting num in a sorted list | Space: O(n)
    def insert_num(self, num):
        if not self.first_half or num <= -self.first_half[0]:
            heappush(self.first_half, -num)
        else:
            heappush(self.second_half, num)

        # either both the heaps will have equal number of elements or max-heap will have one
        # more element than the min-heap
        # balance the two heaps
        if len(self.first_half) - len(self.second_half) > 1:
            heappush(self.second_half, -heappop(self.first_half))
        # since we made the design choice that max_heap will have the extra element
        elif len(self.second_half) > len(self.first_half):
            heappush(self.first_half, -heappop(self.second_half))

    # Time: O(1) | Space: O(1)
    def find_median(self):
        # we have even number of elements, take the average of middle two elements
        if len(self.first_half) == len(self.second_half):
            return (-self.first_half[0] + self.second_half[0]) / 2
        # because max-heap will have one more element than the min-heap
        return -self.first_half[0] / 1.0


def main():
    medianOfAStream = MedianOfAStream()
    medianOfAStream.insert_num(3)
    medianOfAStream.insert_num(1)
    print("The median is: " + str(medianOfAStream.find_median()))
    medianOfAStream.insert_num(5)
    print("The median is: " + str(medianOfAStream.find_median()))
    medianOfAStream.insert_num(4)
    print("The median is: " + str(medianOfAStream.find_median()))


main()
