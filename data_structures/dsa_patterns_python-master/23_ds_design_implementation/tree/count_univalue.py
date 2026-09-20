from tree.bst_print import TreeNode

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def __init__(self):
        self.count_univalue = 0

    def countUnivalSubtrees(self, root: TreeNode) -> int:
        if not root:
            return 0
        if self.isUnivalSubtree(root, root.val):
            self.count_univalue += 1
        self.countUnivalSubtrees(root.left)  # updating global var, not counting
        self.countUnivalSubtrees(root.right)  # updating global var, not counting
        return self.count_univalue

    def isUnivalSubtree(self, root, val):
        if root is None:
            return True
        if root.val != val:
            return False
        return self.isUnivalSubtree(root.left, val) and self.isUnivalSubtree(root.right, val)


# Add test cases - works in Leetcode