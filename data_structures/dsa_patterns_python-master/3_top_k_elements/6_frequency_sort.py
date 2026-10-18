# Copyright © 2020 way2FAANG
# LeetCode: 451


from heapq import heappush, heappop


# Time: O(d*log(d)), d - distinct chars. Worst case: O(n*log(n)) | Space: O(1)
def sort_character_by_frequency(str):
    char_freq_map = {}
    for char in str:
        char_freq_map[char] = char_freq_map.get(char, 0) + 1

    max_heap = []

    for char, freq in char_freq_map.items():
        heappush(max_heap, (-freq, char))  # -ive since we want max heap

    # we could also sort the char_freq_map based on frequency
    # output var
    result = []
    while max_heap:
        freq, char = heappop(max_heap)

        # remember negative freq was inserted in heap
        for _ in range(-freq):
            result.append(char)

    return ''.join(result)


def main():
    print("String after sorting characters by frequency: " +
          sort_character_by_frequency("Programming"))
    print("String after sorting characters by frequency: " +
          sort_character_by_frequency("abcbab"))


main()
