# Copyright © 2020 way2FAANG


from __future__ import print_function
from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def tree_left_view(root):
    # o/p var initialization & input validation
    result = []
    if root is None:
        return result

    # bfs initialization - Define queue for BFS and add root
    queue = deque()
    queue.append(root)

    # bfs traversal (main loop) - Iterate till queue is empty
    while queue:
        # **At the start of each iteration, queue will contain nodes belonging to the same level
        current_level_size = len(queue)

        # current level traversal
        for i in range(current_level_size):
            # Get the first node in queue
            current_node = queue.popleft()

            # ** First node in the current level will be part of left view of the tree
            if i == 0:
                result.append(current_node)

            # Add children
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

    return result


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    root.left.left.left = TreeNode(3)
    result = tree_left_view(root)
    print("Tree right view: ")
    for node in result:
        print(str(node.val) + " ", end='')


if __name__ == '__main__':
    main()
