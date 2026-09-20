# Copyright © 2020 way2FAANG

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
# first write the code to reverse like previous problem
# then add a flag
# add code to skip and reverse flag
# don't forget to break out of main loop in common code
def reverse_alternate_k_elements(head, k):
    # Input validation
    if k <= 1 or head is None:
        return head

    reverse = True
    previous, current = None, head
    while current:
        i = 0
        # reverse next k element sublist
        if reverse:
            last_node_first_part = previous
            last_node_sublist_reverse = current

            while current and i < k:
                next_ = current.next
                current.next = previous
                previous = current
                current = next_
                i += 1

            first_node_sublist_reverse = previous
            first_node_third_part = current

            if last_node_first_part:
                last_node_first_part.next = first_node_sublist_reverse
            else:
                head = first_node_sublist_reverse

            last_node_sublist_reverse.next = first_node_third_part

            previous = last_node_sublist_reverse
        # keep next k element sublist as it is (dont reverse)
        else:
            while current and i < k:
                previous = current
                current = current.next
                i += 1

        reverse = not reverse

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
    result = reverse_alternate_k_elements(head, 2)
    print("Nodes of reversed LinkedList are: ", end='')
    result.print_list()


main()
