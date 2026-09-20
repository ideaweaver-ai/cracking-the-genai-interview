from tree.bst_print import TreeNode
from typing import List


class Solution:
    def __init__(self):
        # Need global var to track preorder index to create current root
        self.pre_index = 0

    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        def buildTreeHelper(in_start, in_end):
            # right helper function as a nested function to prevent passing inorder, postorder and node_index_map in each call
            if in_start > in_end:
                return None

            ## Create root
            root_val = preorder[self.pre_index]
            root = TreeNode(root_val)
            self.pre_index += 1

            ## Create left and right subtrees
            root_index = node_index_map.get(root_val)

            # since preorder, left then right
            root.left = buildTreeHelper(in_start, root_index - 1)
            root.right = buildTreeHelper(root_index + 1, in_end)

            return root

        node_index_map = {val: index for index, val in enumerate(inorder)}
        return buildTreeHelper(0, len(inorder) - 1)
