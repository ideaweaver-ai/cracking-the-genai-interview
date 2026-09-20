# Copyright © 2020 way2FAANG

# LeetCode: 116


from __future__ import print_function
from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right, self.next = None, None, None

    # level order traversal using 'next' pointer
    def print_level_order(self):
        nextLevelRoot = self
        while nextLevelRoot:
            current = nextLevelRoot
            nextLevelRoot = None
            while current:
                print(str(current.val) + " ", end='')
                if not nextLevelRoot:
                    if current.left:
                        nextLevelRoot = current.left
                    elif current.right:
                        nextLevelRoot = current.right
                current = current.next
            print()


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def connect_level_order_siblings(root):
    # Input validation
    if not root:
        return

    # bfs initialization - Define queue for BFS and add root
    queue = deque()
    queue.append(root)

    # bfs traversal (main loop) - Iterate till queue is empty
    while queue:
        # **At the start of each iteration, queue will contain nodes belonging to the same level
        current_level_size = len(queue)
        for i in range(current_level_size):
            current_node = queue.popleft()

            # Check if node is last node before connecting to sibling
            if i != current_level_size - 1:
                current_node.next = queue[0]
                # next is already initialized to None, no need to connect last node in level to None

            # Add children
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

    # this problem does not ask to return root, if problem asks to return root then do so


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    connect_level_order_siblings(root)

    print("Level order traversal using 'next' pointer: ")
    root.print_level_order()


if __name__ == '__main__':
    main()
