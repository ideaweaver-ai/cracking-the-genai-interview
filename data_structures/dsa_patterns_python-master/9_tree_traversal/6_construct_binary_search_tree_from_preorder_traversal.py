# Copyright © 2020 way2FAANG
# LeetCode: 1008

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
        self.index = 0

    # Time : O(n) | Space: O(n)
    def bstFromPreorder(self, preorder: List[int]) -> TreeNode:
        def bstFromPreorderHelper(lower, higher):
            """Returning root of the tree constructed by placing nodes from preorder between range of values"""
            # base cases
            if self.index == n:
                return None

            # Process current node
            root_val = preorder[self.index]

            # # base case 2
            if root_val < lower or root_val > higher:
                return None

            root = TreeNode(root_val)
            self.index += 1

            # since preorder, left then right
            root.left = bstFromPreorderHelper(lower, root_val)
            root.right = bstFromPreorderHelper(root_val, higher)

            return root

        # main function
        n = len(preorder)
        tree_root = bstFromPreorderHelper(-float('inf'), float('inf'))
        return tree_root


if __name__ == '__main__':
    preorder = [8, 5, 1, 7, 10, 12]
    sol = Solution()
    root = sol.bstFromPreorder(preorder)
    print(root.display())
