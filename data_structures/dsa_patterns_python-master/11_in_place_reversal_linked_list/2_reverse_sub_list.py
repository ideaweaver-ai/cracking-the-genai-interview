# Copyright © 2020 way2FAANG
# LeetCode: 206

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


# we are interested in three parts of the LinkedList
# the part before index 'p',the part between 'p' and 'q', and the part after index 'q'
# first part -> sub list reversed -> last part
# skip first p-1 nodes
# store last node of first part, last node of sublist (after reverse) to connect to sub list after reversing
# reverse sub list
# store first node of sub list (after reverse) and first node of third part
# connect last node of first part to first node of sub list (after reverse)
# connect last node of sub list (after reverse) to first node of last part

def reverse_sub_list(head, p, q):
    # skip p-1 nodes
    i = 0
    previous, current = None, head

    while current and i < p - 1:
        previous = current
        current = current.next
        i += 1

    # store last node of first part, last node of sublist to connect to sub list after reversing
    last_node_of_first_part = previous
    last_node_of_sublist_after_reverse = current

    # Check - Nothing to reverse
    if not current:
        return head

    # reverse sub list
    i = 0
    while current and i < q - p + 1:
        next_ = current.next
        current.next = previous
        previous = current
        current = next_
        i += 1

    # store first node of sub list (after reverse) and first node of third part
    first_node_of_sub_list_after_reverse = previous
    first_node_of_third_part = current

    # connect last node of first part to first node of sub list (after reverse)
    if last_node_of_first_part:
        last_node_of_first_part.next = first_node_of_sub_list_after_reverse
    else:
        # p = 1, reversing from head
        head = first_node_of_sub_list_after_reverse

        # connect last node of sub list (after reverse) to first node of last part
    last_node_of_sublist_after_reverse.next = first_node_of_third_part

    return head


def main():
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)

    print("Nodes of original LinkedList are: ", end='')
    head.print_list()
    result = reverse_sub_list(head, 2, 4)
    print("Nodes of reversed LinkedList are: ", end='')
    result.print_list()


main()
