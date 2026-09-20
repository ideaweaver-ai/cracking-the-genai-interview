# Copyright © 2020 way2FAANG
# LeetCode: 767


from heapq import *


# Time: O(n*log(n)) | Space: O(n)
# To have the best chance of not having same letter together, we always want to place the char with max freq first
# Hence we need max heap
# Also once we place a char in result, to fill next spot of result we cannot use this char
# Hence we store it outside the max heap for next iteration
def rearrange_string(str):
    # Create character frequency map
    char_freq_map = {}
    for char in str:
        char_freq_map[char] = char_freq_map.get(char, 0) + 1

    # Insert all elements in max heap
    max_heap = []
    for char, freq in char_freq_map.items():
        heappush(max_heap, (-freq, char))

    result = []
    # to keep max frequncy and char out of heap for 1 iteration
    previous_char, previous_freq = None, 0

    while max_heap:
        # Pop the char with max freq
        freq, char = heappop(max_heap)
        result.append(char)
        freq += 1  # decrease freq
        # First push previous max into heap
        # It can be part of result it was out of the heap for 1 iteration
        if previous_char and -previous_freq > 0:
            heappush(max_heap, (previous_freq, previous_char))
        # Store current max in previous
        previous_char, previous_freq = char, freq

    return "".join(result) if len(result) == len(str) else ""


def main():
    print("Rearranged string:  " + rearrange_string("aappp"))
    print("Rearranged string:  " + rearrange_string("Programming"))
    print("Rearranged string:  " + rearrange_string("aapa"))


main()
