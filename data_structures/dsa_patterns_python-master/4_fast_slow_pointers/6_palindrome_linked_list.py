# Copyright © 2020 way2FAANG
# LeetCode: 234


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


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


# 1 find middle ( dont need previous because it is still connected)
# 2 reverse 2nd half
# 3 keep copy of head of 2nd half reversed and also head
# 4 check palindrome
# 5 reverse second half again to put LL back into place
def is_palindromic_linked_list(head):
    # o/p
    is_palindrome = True

    # 1 find middle
    middle = find_middle(head)

    # 2 reverse second half
    head2 = reverse(middle)

    # 3 copy 2nd half head
    head2_copy = head2
    head_copy = head

    # 4 check palindrome
    while head2:
        if head.value != head2.value:  # imp - don't compare nodes directly
            is_palindrome = False
            break  # we cannot return because we need to make the LL as give at start
        head = head.next
        head2 = head2.next

    # 5 reverse second half again
    # No need to connect as prevof middle is still connected to midlle
    # we just need to reverse pointers
    reverse(head2_copy)

    return is_palindrome


def main():
    head = Node(2)
    head.next = Node(4)
    head.next.next = Node(6)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(2)

    print("Is palindrome: " + str(is_palindromic_linked_list(head)))

    head.next.next.next.next.next = Node(2)
    print("Is palindrome: " + str(is_palindromic_linked_list(head)))


main()
