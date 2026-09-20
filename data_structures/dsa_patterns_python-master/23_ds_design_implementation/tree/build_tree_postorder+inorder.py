from tree.bst_print import TreeNode
from typing import List


class Solution:
    def __init__(self):
        # we need a global index for postorder to find current root from postorder
        self.post_index = -1  # since last element is the root

    def buildTree(self, inorder: List[int], postorder: List[int]) -> TreeNode:
        def buildTreeHelper(in_start, in_end):
            # base case
            if in_start > in_end:
                return None

            ## Create root
            # Last index in postorder is the root
            root_val = postorder[self.post_index]
            root = TreeNode(root_val)
            self.post_index -= 1

            ## Create left and right subtrees
            # find index of root in inorder to find left sub tree and right sub tree
            root_index = node_index_map[root_val]


            # Recursive calls to buld the sub trees
            # right first and then left because if you check postore from end it is root, right, left
            root.right = buildTreeHelper(root_index + 1, in_end)
            root.left = buildTreeHelper(in_start, root_index - 1)

            return root

        node_index_map = {val: index for index, val in enumerate(inorder)}
        root = buildTreeHelper(0, len(inorder) - 1)
        return root
