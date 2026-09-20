# Copyright © 2020 way2FAANG
# LeetCode: 105

from typing import List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def display(self):
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.val
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class Solution:
    def __init__(self):
        # Need global var to track preorder index to create current root
        # At current node - right sided subtree needs updated preorder index from left sided subtree
        self.preorder_index = 0

    # Time: O(n) | Space: O(n)
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        def buildTreeHelper(start_inorder, end_inorder):
            """Construct a subtree using preorder and inorder and returns its root.
            Consider nodes in inorder between start_inorder and end_inorder indices"""
            # write helper function as an inner function
            # to prevent passing inorder, postorder and node_index_map in each call
            if start_inorder > end_inorder or self.preorder_index >= len(preorder):
                return None

            # Process current node
            root_val = preorder[self.preorder_index]
            root = TreeNode(root_val)
            self.preorder_index += 1

            # Create left and right subtrees
            root_inorder_index = node_val_inorder_index_map.get(root_val)

            # since preorder, left then right
            root.left = buildTreeHelper(start_inorder, root_inorder_index - 1)
            root.right = buildTreeHelper(root_inorder_index + 1, end_inorder)

            return root

        node_val_inorder_index_map = {val: index for index, val in enumerate(inorder)}
        return buildTreeHelper(0, len(inorder) - 1)


if __name__ == '__main__':
    preorder = [3, 9, 20, 15, 7]
    inorder = [9, 3, 15, 20, 7]
    sol = Solution()
    root = sol.buildTree(preorder, inorder)
    print(root.display())
