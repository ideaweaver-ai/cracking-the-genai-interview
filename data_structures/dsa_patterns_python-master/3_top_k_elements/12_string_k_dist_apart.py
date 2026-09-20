# Copyright © 2020 way2FAANG
# LeetCode: 358


from heapq import heappush, heappop

# def reorganize_string(str, k):
#     char_freq_map = {}
#     for char in str:
#         char_freq_map[char] = char_freq_map.get(char, 0) + 1
#
#     max_heap = []
#     for char, freq in char_freq_map.items():
#         heappush(max_heap, (-freq, char))
#
#     previous = [None] * (k - 1)
#     result = []
#     i = 0
#
#     while max_heap:
#         # print(result)
#         # print(max_heap)
#         # print(previous)
#         freq, char = heappop(max_heap)
#         result.append(char)
#         freq += 1
#         if previous[i] is not None:
#             heappush(max_heap, previous[i])
#         if freq != 0:
#             previous[i] = (freq, char)
#         else:
#             previous[i] = None
#         i += 1
#         i %= (k - 1)
#
#     return ''.join(result)
#
#     return ""


# Time: O(n*log(n)) | Space: O(n)
from heapq import heappush, heappop
from collections import deque


def reorganize_string(str, k):
    char_freq_map = {}
    for char in str:
        char_freq_map[char] = char_freq_map.get(char, 0) + 1

    # We should append the char with max freq to result
    # This will give us best chance of creting string where a char is not adjacent to itself
    # Hence use max heap
    max_heap = []
    for char, freq in char_freq_map.items():
        heappush(max_heap, (-freq, char))

    result = []
    queue = deque()  # since want to keep a char out of max heap for 'k' cycles
    while max_heap:
        freq, char = heappop(max_heap)
        result.append(char)
        # but we dont push this char back into heap
        # as we dont want it to be popped in the next iteration
        # this will ensure we dont get a char adjacent to itself
        freq += 1  # decrement freq
        queue.append((freq, char))
        # if len of queue is k, the first char has waited for k chars
        # which means the next k-1 chars following it in result are different
        # so it can be considered for next iteration and can enter max heap
        if len(queue) == k:
            prev_freq, prev_char = queue.popleft()
            # we could have done this check while inserting in queue - but that would be wrong
            # check e.g. element having freq 1 when you pop, the element should go in queue an increment len by 1
            # that way the first char in queue will correctly wait for k-1 chars after it in result
            if -prev_freq > 0:
                heappush(max_heap, (prev_freq, prev_char))
    return "".join(result) if len(result) == len(str) else ""


def main():
    print("Reorganized string: " + reorganize_string("mmpp", 2))
    print("Reorganized string: " + reorganize_string("Programming", 3))
    print("Reorganized string: " + reorganize_string("aab", 2))
    print("Reorganized string: " + reorganize_string("aapa", 3))


main()