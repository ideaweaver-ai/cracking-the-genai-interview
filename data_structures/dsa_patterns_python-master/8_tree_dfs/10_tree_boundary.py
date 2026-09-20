# Copyright © 2020 way2FAANG
# LeetCode: 545

from __future__ import print_function
from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


# def find_leaves(root):
#     leaves = []
#     helper(root, leaves)
#     # leaves passed by reference and modified in the function
#     return leaves


def find_leaves_helper(current_node, leaves):
    # base case
    if current_node is None:
        return

    # base case 2
    if current_node.left is None and current_node.right is None:
        leaves.append(current_node)

    # recursion calls
    find_leaves_helper(current_node.left, leaves)
    find_leaves_helper(current_node.right, leaves)


def find_tree_boundary(root):
    if root is None:
        return []
    left_view, right_view = [], deque()
    queue = deque()
    queue.append(root)
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            current_node = queue.popleft()
            # Ignore leaf nodes. They will be taken care as part of leaves
            if not current_node.left and not current_node.right:
                continue
            if i == 0:
                left_view.append(current_node)
            elif i == level_size - 1:
                right_view.appendleft(current_node)

            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
    # dfs to get leaves
    leaves = []
    find_leaves_helper(root, leaves)
    return left_view + leaves + list(right_view)


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(4)
    root.left.left.left = TreeNode(9)
    root.left.right = TreeNode(3)
    root.left.right.left = TreeNode(15)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    root.right.right.left = TreeNode(6)
    result = find_tree_boundary(root)
    print("Tree boundary: ", end='')
    for node in result:
        print(str(node.val) + " ", end='')


main()
