from heapq import heappush, heappop
from tree.bst_print import TreeNode

# Leetcode # 230
# DS refresher - 2

# Follow up
# What if the BST is modified (insert/delete operations) often and you need to find the kth smallest frequently?
# How would you optimize the kthSmallest routine?

# Using heap
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def __init__(self):
        self.max_heap = []  # this will help for for the follow up

    # using heap
    # def kthSmallest(self, root: TreeNode, k: int) -> int:
    #     self.kth_smallest_helper(root, k)
    #     if len(self.max_heap) < k:
    #         return None
    #     return -self.max_heap[0]  # since for max heap we push negative nos
    #
    # def kth_smallest_helper(self, root, k):
    #     if root is None:
    #         return
    #     heappush(self.max_heap, -root.val)
    #     if len(self.max_heap) > k:
    #         heappop(self.max_heap)
    #     self.kth_smallest_helper(root.left, k)
    #     self.kth_smallest_helper(root.right, k)

    # Using inorder

    def kthSmallest(self, root: TreeNode, k: int) -> int:
        self.kth_smallest_helper(root, k)
        if len(self.tree_list) < k:
            return None
        return self.tree_list[k - 1]  # since for max heap we push negative nos

    def kth_smallest_helper(self, root, k):
        # Inorder traversal - as it sorts the tree into ascending order
        if root is None:
            return
        self.kth_smallest_helper(root.left, k)
        self.tree_list.append(root.val)
        self.kth_smallest_helper(root.right, k)


if __name__ == '__main__':
    # Build Tree for testing
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(6)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.left.left.left = TreeNode(1)
    soln = Solution()
    print(soln.kthSmallest(root, 3))
