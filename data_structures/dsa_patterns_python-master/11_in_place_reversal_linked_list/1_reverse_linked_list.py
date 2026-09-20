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


# Time: O(n) | Space: O(1)
def reverse(head):
    # we need reference to 2 nodes to reverse the LL connection
    previous, current = None, head
    while current:
        next_ = current.next  # store the next node before point to previous
        current.next = previous  # reverse current node
        previous = current  # current node becomes previous
        current = next_  # next node becomes current
    return previous


def main():
    head = Node(2)
    head.next = Node(4)
    head.next.next = Node(6)
    head.next.next.next = Node(8)
    head.next.next.next.next = Node(10)

    print("Nodes of original LinkedList are: ", end='')
    head.print_list()
    result = reverse(head)
    print("Nodes of reversed LinkedList are: ", end='')
    result.print_list()


main()
