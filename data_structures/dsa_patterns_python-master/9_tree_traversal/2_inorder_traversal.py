from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # Time: O(n) | Space: O(n)

    # recursive
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        self.inorderTraversalHelper(root, result)
        return result

    # recursive helper
    def inorderTraversalHelper(self, root: TreeNode, result: List) -> None:
        # base case
        if root is None:
            return
        # inorder - process current node and recursive calls
        self.inorderTraversalHelper(root.left, result)
        result.append(root.val)
        self.inorderTraversalHelper(root.right, result)

    # iterative
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        # o/p var and i/p validation
        result = []
        if not root:
            return result

        # init stack
        stack = []
        current_node = root

        while current_node or stack:
            # go left till you have current node
            while current_node:
                stack.append(current_node)
                current_node = current_node.left

            # at this execution, we have reached the leftmost node
            # **imp - append current node to result and go right
            current_node = stack.pop()
            result.append(current_node.val)
            # ** go right
            current_node = current_node.right

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
    print(sol.inorderTraversal(root))

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    sol = Solution()
    print(sol.inorderTraversal(root))

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.left.right = TreeNode(11)
    root.left.left.right.left = TreeNode(12)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    sol = Solution()
    print(sol.inorderTraversal(root))
