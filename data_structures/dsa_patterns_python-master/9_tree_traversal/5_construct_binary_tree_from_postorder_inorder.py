# Copyright © 2020 way2FAANG
# LeetCode: 106

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
        # we need a global index for postorder to find current root from postorder
        self.postorder_index = -1  # since last element is the root

    # Time: O(n) | Space: O(n)
    def buildTree(self, inorder: List[int], postorder: List[int]) -> TreeNode:
        def buildTreeHelper(start_inorder, end_inorder):
            """Construct a subtree using inorder and postorder and returns its root.
            Consider nodes in inorder between start_inorder and end_inorder indices"""
            # base case
            if start_inorder > end_inorder or self.postorder_index < -len(postorder):
                return None

            # Process current node
            # Last index in postorder is the root
            root_val = postorder[self.postorder_index]
            root = TreeNode(root_val)
            self.postorder_index -= 1

            # find index of root in inorder to find left sub tree and right sub tree
            root_inorder_index = node_index_map[root_val]

            # Recursive calls to build the sub trees
            # right first and then left because if you check postorder from end it is root, right, left
            root.right = buildTreeHelper(root_inorder_index + 1, end_inorder)
            root.left = buildTreeHelper(start_inorder, root_inorder_index - 1)

            return root

        # main function
        if len(inorder) != len(postorder):
            return None

        node_index_map = {val: index for index, val in enumerate(inorder)}
        root = buildTreeHelper(0, len(inorder) - 1)
        return root


if __name__ == '__main__':
    inorder = [9, 3, 15, 20, 7]
    postorder = [9, 15, 7, 20, 3]
    sol = Solution()
    root = sol.buildTree(inorder, postorder)
    print(root.display())
