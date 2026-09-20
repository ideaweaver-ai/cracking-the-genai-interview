# Copyright © 2020 way2FAANG
# LeetCode: 895


from heapq import *


class Element:

    def __init__(self, number, frequency, sequenceNumber):
        self.number = number
        self.frequency = frequency
        self.sequenceNumber = sequenceNumber

    def __lt__(self, other):
        # higher frequency wins
        if self.frequency != other.frequency:
            return self.frequency > other.frequency
        # if both elements have same frequency, return the element that was pushed later
        return self.sequenceNumber > other.sequenceNumber


class FrequencyStack:
    def __init__(self):

        # our input is in online
        # We want to pop the element with max freq in log(n) vs O(n) if sorted
        self.max_heap = []
        # to get current frequency of the num being pushed in O(1)
        # else we will have to scan the max_heap to find the element's current frequency - O(n)
        self.num_freq_map = {}
        # to find which element is pushed later when frequency is same (max frequency)
        self.sequence = 0

    def push(self, num):
        self.num_freq_map[num] = self.num_freq_map.get(num, 0) + 1
        heappush(self.max_heap, Element(
            num, self.num_freq_map[num], self.sequence))
        self.sequence += 1

    def pop(self):
        num = None
        if self.max_heap:
            num = heappop(self.max_heap).number
            # decrement the frequency or remove if this is the last number
            if self.num_freq_map[num] > 1:
                self.num_freq_map[num] -= 1
            else:
                del self.num_freq_map[num]

        return num


def main():
    freq_stack = FrequencyStack()
    freq_stack.push(1)
    freq_stack.push(2)
    freq_stack.push(3)
    freq_stack.push(2)
    freq_stack.push(1)
    freq_stack.push(2)
    freq_stack.push(5)
    print(freq_stack.pop())
    print(freq_stack.pop())
    print(freq_stack.pop())


main()
