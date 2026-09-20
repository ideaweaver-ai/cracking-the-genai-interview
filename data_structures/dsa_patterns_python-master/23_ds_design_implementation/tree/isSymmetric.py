from tree.bst_print import TreeNode


class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        return self.isSymmetricHelper(root, root)

    def isSymmetricHelper(self, root1, root2):
        if root1 is None and root2 is None:
            return True
        if root1 is None or root2 is None:  # only 1 root is Non None
            return False
        return (root1.val == root2.val) and self.isSymmetricHelper(root1.left, root2.right) and self.isSymmetricHelper(
            root1.right, root2.left)


# Add test case - works in leetcode