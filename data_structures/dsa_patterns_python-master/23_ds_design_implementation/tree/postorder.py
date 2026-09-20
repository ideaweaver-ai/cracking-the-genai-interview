from tree.bst_print import TreeNode
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
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

    def postorderTraversal(self, root):
        result, stack = [], []
        current_node = root
        while current_node or stack:
            while current_node:
                # Stack is LIFO
                # Why push both nodes, why not just right as that is the next node in postorder
                # Because in inorder we could go current_node = current_node.right later wehen we pop from stack
                # We cannot go back to parent if we were to just put right node

                # Ideally we want to push current and then right (for postorder)
                # Check the logic when we pop from stack to why we dont do this
                if current_node.right is not None:
                    stack.append(current_node.right)
                stack.append(current_node)

                # Similar to inorder we ant to keep going left if we can
                current_node = current_node.left
            # Reached the left most element in the branch
            current_node = stack.pop()

            # If the popped item has a right child and the right child is not processed yet,
            # then we need to process the right child before root
            # To check that we peek stack (the if condition)
            # Going back - hence we push right child and then current node earlier, so we could check this
            if current_node.right is not None and current_node.right == self.peek(stack):
                # need to process right child first. it is unprocessed since it's in the stack
                stack.pop()  # it will be put in stack above the root on the 'while current_node' loop
                stack.append(current_node)
                current_node = current_node.right  # similar to inorder

            else:
                result.append(current_node.val)
                current_node = None  # very imp, in this case we are not setting to right. If we don't do this we will be stuck indefinitely
        return result


if __name__ == '__main__':
    # Build Tree for testing
    # Not necessarily a BST. Just named sequentially for easy processing
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(6)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)
    root.right.right.right = TreeNode(8)
    root.display()
    soln = Solution()
    print(soln.postorderTraversal(root))
    root = TreeNode(1)
    root.left = TreeNode(None)
    root.right = TreeNode(2)
    root.right.left = TreeNode(3)
    print(soln.postorderTraversal(root))

