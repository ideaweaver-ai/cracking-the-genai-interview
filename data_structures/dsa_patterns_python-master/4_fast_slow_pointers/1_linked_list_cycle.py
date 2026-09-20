# Copyright © 2020 way2FAANG
# LeetCode: 141


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


# Time: O(n) | SPace: O(1)
def has_cycle(head):
    slow, fast = head, head

    # if no cycle - fast will reach the end of the Linked List before slow - so while condition needs to be on fast
    # **imp - since we will move fast by two pointers, important to check fast.next is also there
    # if we just check fast in some cases we may get null pointer exception
    #
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # cycle found
            return True

    return False


def main():
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)
    head.next.next.next.next.next = Node(6)
    print("LinkedList has cycle: " + str(has_cycle(head)))

    head.next.next.next.next.next.next = head.next.next
    print("LinkedList has cycle: " + str(has_cycle(head)))

    head.next.next.next.next.next.next = head.next.next.next
    print("LinkedList has cycle: " + str(has_cycle(head)))


main()
