from tree.bst_print import TreeNode
from typing import List


class Solution:
    #     # recursive
    #     def inorderTraversal(self, root: TreeNode) -> List[int]:
    #         result = []
    #         self.inorderTraversalHelper(root, result)
    #         return result

    #     # recursive helper
    #     def inorderTraversalHelper(self, root: TreeNode, result: List) -> None:
    #         if root is None:
    #             return
    #         self.inorderTraversalHelper(root.left, result)
    #         result.append(root.val)
    #         self.inorderTraversalHelper(root.right, result)

    # iterative
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        current_node = root
        stack = []
        while current_node or stack:
            # For pre order put current node and go left if you can
            while current_node:
                stack.append(current_node)
                current_node = current_node.left
            # When I have gone as left as possible I pop and process the node
            current_node = stack.pop()
            # If possible now try to put the right branch in stack
            result.append(current_node.val)
            current_node = current_node.right
        return result
