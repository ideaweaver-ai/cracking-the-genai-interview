# Copyright © 2020 way2FAANG

# LeetCode: 111

from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def find_minimum_depth(root):
    # o/p var initialization & input validation
    if root is None:
        return 0

    # bfs initialization - Define queue for BFS and add root
    queue = deque()
    queue.append(root)

    # track current depth
    current_level_depth = 0

    # bfs traversal (main loop) - Iterate till queue is empty
    while queue:
        # **At the start of each iteration, queue will contain nodes belonging to the same level
        current_level_size = len(queue)
        # increase current depth
        current_level_depth += 1

        # current level traversal
        for _ in range(current_level_size):
            current_node = queue.popleft()
            # Check if leaf - ** As we are traversing level by level the first leaf node should give min depth
            if current_node.left is None and current_node.right is None:
                return current_level_depth

            # Add children
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    print("Tree Minimum Depth: " + str(find_minimum_depth(root)))
    root.left.left = TreeNode(9)
    root.right.left.left = TreeNode(11)
    print("Tree Minimum Depth: " + str(find_minimum_depth(root)))


if __name__ == '__main__':
    main()