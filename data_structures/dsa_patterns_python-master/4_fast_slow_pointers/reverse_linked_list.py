class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def reverse(head):
    prev = None
    while head:
        next = head.next
        head.next = prev
        prev = head
        head = next
    return prev


if __name__ == '__main__':
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)

    # original linked list
    head_copy = head
    print('Original LL')
    while head_copy:
        print(head_copy.value, end='->')
        head_copy = head_copy.next
    print()

    # print reverse
    head_copy = reverse(head)
    print('Reversed LL')
    while head_copy:
        print(head_copy.value, end='->')
        head_copy = head_copy.next
