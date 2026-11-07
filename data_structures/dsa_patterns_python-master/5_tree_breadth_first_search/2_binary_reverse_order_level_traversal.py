# Copyright © 2020 way2FAANG

# LeetCode: 107

from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def traverse(root):
    # o/p var initialization & input validation
    result = deque()
    if root is None:
        return []  # don't return result as it is deque and not list object

    # bfs initialization - Define queue for BFS and add root
    queue = deque()
    queue.append(root)

    # bfs traversal (main loop) - Iterate till queue is empty
    while queue:
        # **At the start of each iteration, queue will contain nodes belonging to the same level
        current_level_size = len(queue)
        # Define list to hold current level nodes
        current_level = []

        # current level traversal
        for _ in range(current_level_size):
            # Get the first node in queue
            current_node = queue.popleft()
            # Add current node to current level
            current_level.append(current_node.val)
            # Add children of the current node  to queue
            # Check if None before adding, otherwise result will have empty elements
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        # Level done, append it to result
        result.appendleft(current_level)

    # need to convert deque to list before returning - O(n) operation. Overall TC remains same
    return list(result)


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    print("Level order traversal: " + str(traverse(root)))


if __name__ == '__main__':
    main()
