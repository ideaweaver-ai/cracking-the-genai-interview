# Copyright © 2020 way2FAANG
# LeetCode: 61

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


# Assume LL length is n. rotation by k means -> ll sublist of n-k nodes moving to the end
# find last node of linked list and count length of linked list
# connect last node of LL to head to make it circular
# calculate last node of rotated LL -> it's next node should be head
# make last node of rotate LL next to None

# Time: O(n) | Space: O(1)
def rotate(head, rotations):
    if not head or not head.next or rotations == 0:
        return head

    length = 0
    prev, current = None, head
    while current:
        prev = current
        current = current.next
        length += 1

    # make ll circular
    prev.next = head
    # rotations should be <= linked list length
    rotations %= length

    # calculate skip length to find last of rotated linked list
    skip_length = length - rotations
    prev, current = None, head
    for _ in range(skip_length):  # because we are already at head, we need to do skip_length - 1 iterations
        prev = current
        current = current.next

    # current will be the rotated list's head
    tail_rotated_list = prev
    head_rotated_list = current

    # adjust pointers
    tail_rotated_list.next = None

    return head_rotated_list


def main():
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)
    head.next.next.next.next.next = Node(6)

    print("Nodes of original LinkedList are: ", end='')
    head.print_list()
    result = rotate(head, 3)
    print("Nodes of rotated LinkedList are: ", end='')
    result.print_list()


main()
