# Copyright © 2020 way2FAANG

# LeetCode: 103

from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def traverse(root):
    # o/p var initialization & input validation
    result = []
    queue = deque()
    queue.append(root)

    # ** imp - traversal direction
    is_left_to_right = True

    # bfs traversal (main loop) - Iterate till queue is empty
    while queue:
        # **At the start of each iteration, queue will contain nodes belonging to the same level
        current_level_size = len(queue)
        current_level = deque()

        # current level traversal
        for _ in range(current_level_size):
            # Get the first node in queue
            current_node = queue.popleft()

            # Process the node
            if is_left_to_right:
                current_level.append(current_node.val)
            else:
                current_level.appendleft(current_node.val)

            # Add children of the current node  to queue
            # Check if None before adding, otherwise result will have empty elements
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        # Level done, ** convert level to list and then add to result
        result.append(list(current_level))
        # reverse traversal direction
        is_left_to_right = not is_left_to_right

    return result


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    root.right.left.left = TreeNode(20)
    root.right.left.right = TreeNode(17)
    print("Zigzag traversal: " + str(traverse(root)))


if __name__ == '__main__':
    main()
