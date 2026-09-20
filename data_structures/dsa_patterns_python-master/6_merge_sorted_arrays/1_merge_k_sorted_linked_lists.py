# Copyright © 2020 way2FAANG
# LeetCode: 23

from __future__ import print_function
from heapq import *


class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __lt__(self, other):
        return self.value < other.value


# Time: O(n*log(k)) | Space: O(k)
def merge_lists(lists):
    result_head, result_tail = None, None

    # 1 Add smallest element of each linked list to heap
    min_heap = []
    for head in lists:
        heappush(min_heap, head)

    # 2 keep on getting the next min amongst all linked lists
    while min_heap:
        # Get the smallest node from all lists
        smallest_node = heappop(min_heap)

        # Append it to result
        if result_head is None:
            result_head = smallest_node
            result_tail = smallest_node
        else:
            result_tail.next = smallest_node
            result_tail = result_tail.next

        # 3 check if current smallest node's linked list has next element and insert it into heap
        if smallest_node.next:
            heappush(min_heap, smallest_node.next)

        # **Important note - We append the smallest node to result tail
        # In next interation we will modify its next pointer. Cause of worry is we may lose the next element in that list
        # Since we are adding the next node to min heap immediately in the next statement, we are good

    return result_head


def main():
    l1 = ListNode(2)
    l1.next = ListNode(6)
    l1.next.next = ListNode(8)

    l2 = ListNode(3)
    l2.next = ListNode(6)
    l2.next.next = ListNode(7)

    l3 = ListNode(1)
    l3.next = ListNode(3)
    l3.next.next = ListNode(4)

    result = merge_lists([l1, l2, l3])
    print("Here are the elements form the merged list: ", end='')
    while result != None:
        print(str(result.value) + " ", end='')
        result = result.next


main()

