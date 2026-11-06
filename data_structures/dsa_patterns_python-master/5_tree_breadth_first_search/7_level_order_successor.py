# Copyright © 2020 way2FAANG

from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


# Time O(n) | Additional Space (for queue): O(n/2) = O(n)
def find_successor(root, key):
    # Input validation
    if not root:
        return None

    # bfs initialization - Define queue for BFS and add root
    queue = deque()
    queue.append(root)

    # bfs traversal (main loop) - Iterate till queue is empty
    while queue:
        # Don't need to keep track of level for this question
        current_node = queue.popleft()
        # Imp -  First add children then check otherwise you may return None even though there is a successor
        # for e.g if key is root
        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)

        if current_node.val == key:
            # Check if key has become empty after popping current node
            # successor is the 0th element in the queue
            break  # optimized code, could return here too
    return queue[0] if queue else None


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.right.left = TreeNode(10)

    root.right.right = TreeNode(5)
    result = find_successor(root, 12)
    if result:
        print(result.val)
    result = find_successor(root, 9)
    if result:
        print(result.val)


if __name__ == '__main__':
    main()
