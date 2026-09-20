# Copyright © 2020 way2FAANG
# LeetCode: 143

from __future__ import print_function


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def print_list(self):
        temp = self
        while temp is not None:
            print(str(temp.value) + " ", end='')
            temp = temp.next
        print()


def find_middle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def reverse(head):
    prev = None
    while head:
        next_ = head.next
        head.next = prev
        prev = head
        head = next_
    return prev


# Time: O(n) | Space: O(1)
def reorder(head):
  middle = find_middle(head)
  tail = reverse(middle)
  head1, head2 = head, tail
  while head2 and head2.next:
    next1 = head1.next
    head1.next = head2
    next2 = head2.next
    head2.next = next1
    head1 = next1
    head2 = next2

  return head

# Time: O(n) | Space: O(1)
# def reorder(head):
#     # 1 find middle
#     middle = find_middle(head)
#     # 2 reverse 2nd hald
#     head2 = reverse(middle)
#     # 3 keep copies of both heads
#     copy_head = head
#     copy_head2 = head2
#     # 4 alternate nodes
#     while head and head2:
#         # connect first half head to second half
#         temp = head.next
#         head.next = head2
#         head = temp
#
#         # connect send half head to first
#         temp = head2.next
#         head2.next = head
#         head2 = temp
#
#     # 5 in case of even - last node points to itself
#     # draw last node for even and odd and check
#     if head:
#         head.next = None
#
#     return copy_head


# def insert(head1, head2):
#     next_ = head1.next
#     head1.next = head2
#     head1 = next_
#     return head1, head2

# More modular code
# Time: O(n) | Space: O(1)
# def reorder(head):
#     first_half = True  # to alternate heads of the two parts
#     copy_head = head  # to return
#     middle = find_middle(head)
#     head_second_half = reverse(middle)
#
#     # Imp - don't use break condition head and second_half_head is not None. As both will have  a valid next pointer
#     while head != middle:
#         if first_half:
#             if head:
#                 # first half head to connect to second half head
#                 head, head_second_half = insert(head, head_second_half)
#                 first_half = not first_half
#
#         else:
#             if head_second_half:
#                 head_second_half, head = insert(head_second_half, head)
#                 first_half = not first_half
#
#     return copy_head


def main():
    head = Node(2)
    head.next = Node(4)
    head.next.next = Node(6)
    head.next.next.next = Node(8)
    head.next.next.next.next = Node(10)
    head.next.next.next.next.next = Node(12)
    reorder(head)
    head.print_list()

    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)
    reorder(head)
    head.print_list()


main()
