"""Validate a strict BST using subtree min, max, and validity (98).

Time: O(n); space: O(h). Duplicate values are invalid."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root):
    if root is None:
        return True

    def dfs(node):
        smallest = largest = node.val
        valid = True
        if node.left is None and node.right is None:
            return smallest, largest, valid
        if node.left is not None:
            left_min, left_max, left_valid = dfs(node.left)
            smallest = min(smallest, left_min)
            largest = max(largest, left_max)
            if not left_valid or left_max >= node.val:
                valid = False
        if node.right is not None:
            right_min, right_max, right_valid = dfs(node.right)
            smallest = min(smallest, right_min)
            largest = max(largest, right_max)
            if not right_valid or right_min <= node.val:
                valid = False
        return smallest, largest, valid

    return dfs(root)[2]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(is_valid_bst(root))


if __name__ == "__main__":
    main()
