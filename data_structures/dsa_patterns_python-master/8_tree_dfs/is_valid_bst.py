# Copyright © 2020 way2FAANG
# LeetCode: 98

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# recursive code
# Time: O(n) |
# Space: O(d) where d is depth of the tree, d = n for unbalanced tree, d = log(n) for balanced tree
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def isValidBSTHelper(current_node, lower_limit, upper_limit):
            # base cases
            if current_node is None:
                return True

            # process current_node
            if current_node.val <= lower_limit or current_node.val >= upper_limit:
                return False

            # recursive calls
            is_left_subtree_bst = isValidBSTHelper(current_node.left, lower_limit, current_node.val)
            is_right_subtree_bst = isValidBSTHelper(current_node.right, current_node.val, upper_limit)

            return is_left_subtree_bst and is_right_subtree_bst

        return isValidBSTHelper(root, -float('inf'), float('inf'))


# recursive code
# Time: O(n) |
# Space: O(d) where d is depth of the tree, d = n for unbalanced tree, d = log(n) for balanced tree
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        stack = [(root, -float('inf'), float('inf'))]

        while stack:
            current_node, lower_limit, upper_limit = stack.pop()

            if current_node.val <= lower_limit or current_node.val >= upper_limit:
                return False

            if current_node.left:
                stack.append((current_node.left, lower_limit, current_node.val))

            if current_node.right:
                stack.append((current_node.right, current_node.val, upper_limit))

        return True