# Copyright © 2020 way2FAANG

# LeetCode: 637

from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def find_level_averages(root):
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
        # var to hold level's running sum
        current_level_sum = 0

        # current level traversal
        for _ in range(current_level_size):
            # Get the first node in queue
            current_node = queue.popleft()
            # Add current node to current level
            current_level_sum += current_node.val
            # Add children of the current node  to queue
            # Check if None before adding, otherwise result will have empty elements
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        # Level done, calculate and append its average to result
        result.append(current_level_sum / current_level_size)
    return result


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    print("Level averages are: " + str(find_level_averages(root)))


if __name__ == '__main__':
    main()