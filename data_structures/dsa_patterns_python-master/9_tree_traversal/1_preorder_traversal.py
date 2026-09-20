from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # Time: O(n) | Space: O(n) # function stack (excluding array)
    # recursive
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        self.preorderTraversalHelper(root, result)
        return result

    def preorderTraversalHelper(self, root, result):
        # base case
        if root is None:
            return

        # preorder - process current node and recursion calls
        result.append(root.val)
        self.preorderTraversalHelper(root.left, result)
        self.preorderTraversalHelper(root.right, result)

    # iterative
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        # o/p var & i/p validation
        result = []
        if not root:
            return result

        # initialize stack and add initial values # similar to bfs
        stack = []
        stack.append(root)

        while stack:
            # process current node
            current_node = stack.pop()
            result.append(current_node.val)
            # process children
            # ** imp - similar to bfs but we want left child first and then right child
            # not also with bfs we wont be able to achieve preorder
            # e.g. with bfs for this example we will have [1, 2, 3, 4, 6, 7]
            # since stack is lifo hence we
            if current_node.right:
                stack.append(current_node.right)
            if current_node.left:
                stack.append(current_node.left)

        return result


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    sol = Solution()
    print(sol.preorderTraversal(root))

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    sol = Solution()
    print(sol.preorderTraversal(root))