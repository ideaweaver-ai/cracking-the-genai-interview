from __future__ import print_function


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def print_list(self):
        temp = self
        while temp is not None:
            print(temp.value, end=" ")
            temp = temp.next
        print()

# Copyright © 2020 way2FAANG
# LeetCode: 25


# Time: O(n) | Space: O(1)
def reverse_every_k_elements(head, k):
    # Input validation
    if k <= 1 or head is None:
        return head
    previous, current = None, head

    while current:
        # reverse k element sublist
        i = 0
        last_node_first_part = previous
        last_node_sublist_reverse = current
        while current and i < k:
            next_ = current.next
            current.next = previous
            previous = current
            current = next_
            i += 1

        # update pointers
        first_node_sublist_reverse = previous
        first_node_third_part = current

        if last_node_first_part:
            last_node_first_part.next = first_node_sublist_reverse
        else:
            head = first_node_sublist_reverse

        last_node_sublist_reverse.next = first_node_third_part

        # ** imp - prev is stuck at head of reversed part
        previous = last_node_sublist_reverse

    return head


def main():
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)
    head.next.next.next.next.next = Node(6)
    head.next.next.next.next.next.next = Node(7)
    head.next.next.next.next.next.next.next = Node(8)

    print("Nodes of original LinkedList are: ", end='')
    head.print_list()
    result = reverse_every_k_elements(head, 3)
    print("Nodes of reversed LinkedList are: ", end='')
    result.print_list()


main()
