# Copyright © 2020 way2FAANG


from __future__ import print_function
from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right, self.next = None, None, None

        # tree traversal using 'next' pointer

    def print_tree(self):
        print("Traversal using 'next' pointer: ", end='')
        current = self
        while current:
            print(str(current.val) + " ", end='')
            current = current.next


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def connect_all_siblings(root):
    # Input validation
    if not root:
        return # if we dont return anything python will return None. so this is same as return None

    # bfs initialization - Define queue for BFS and add root
    queue = deque()
    queue.append(root)

    # bfs traversal (main loop) - Iterate till queue is empty
    while queue:
        # we dont need to track level, we just need to connect each node to the next node in bfs

        # Get the first node in queue
        current_node = queue.popleft()

        # **Add children first, we want to connect to next node even if its in next level
        # take the case of root - if we dont add children first it will not be connected to next node
        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)

        # if queue has a node, connect current node to its next node
        if queue:
            current_node.next = queue[0]

    # this problem does not ask to return root, if problem asks to return root then do so


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    connect_all_siblings(root)

    print("Level order traversal using 'next' pointer: ")
    root.print_tree()


if __name__ == '__main__':
    main()
