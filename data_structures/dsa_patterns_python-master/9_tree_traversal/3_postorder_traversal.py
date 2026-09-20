from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # Time: O(n) | Space: O(n)

    # recursive
    #     def postorderTraversal(self, root: TreeNode) -> List[int]:
    #         result = []
    #         self.postorderTraversalHelper(root, result)
    #         return result

    #     def postorderTraversalHelper(self, root, result):
    #         if root is None:
    #             return
    #         self.postorderTraversalHelper(root.left, result)
    #         self.postorderTraversalHelper(root.right, result)
    #         result.append(root.val)

    # iterative
    def peek(self, stack):
        if len(stack) > 0:
            return stack[-1]
        return None

    def postorderTraversal(self, root: TreeNode) -> List[int]:
        # o/p var
        result = []
        if not root:
            return result

        # ** imp - We are calculating reverse of the postorder
        # initialize stack and add initial values # similar to bfs
        stack = []
        stack.append(root)

        while stack:
            # process current node
            current_node = stack.pop()
            result.append(current_node.val)
            # process children
            # ** imp - it should be opposite of preorder
            if current_node.left:
                stack.append(current_node.left)
            if current_node.right:
                stack.append(current_node.right)

        return result[::-1]


    # Iterative another method
    # def postorderTraversal(self, root: TreeNode) -> List[int]:
    #     result = []
    #     if not root:
    #         return result
    #
    #     stack = []
    #     current_node = root
    #
    #     while current_node or stack:
    #         while current_node:
    #             # this order - to know right child not processed
    #             if current_node.right:
    #                 stack.append(current_node.right)
    #             stack.append(current_node)
    #
    #             # go left as possible
    #             current_node = current_node.left
    #
    #         current_node = stack.pop()
    #
    #         # right child is not processed
    #         if current_node.right is not None and current_node.right == self.peek(stack):
    #             stack.pop()
    #             stack.append(current_node)
    #             current_node = current_node.right
    #         else:
    #             result.append(current_node.val)
    #             current_node = None
    #     return result


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    sol = Solution()
    print(sol.postorderTraversal(root))

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    sol = Solution()
    print(sol.postorderTraversal(root))
