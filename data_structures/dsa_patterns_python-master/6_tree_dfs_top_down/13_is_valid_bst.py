"""Validate a strict BST by passing ancestor bounds down. Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root):
    if root is None:
        return True
    valid = [True]

    def dfs(node, lower, upper):
        if not lower < node.val < upper:
            valid[0] = False
            return
        if node.left is not None:
            dfs(node.left, lower, node.val)
        if node.right is not None:
            dfs(node.right, node.val, upper)

    dfs(root, float("-inf"), float("inf"))
    return valid[0]


def is_valid_bst_iterative(root):
    if root is None:
        return True
    stack = [(root, float("-inf"), float("inf"))]
    while stack:
        node, lower, upper = stack.pop()
        if not lower < node.val < upper:
            return False
        if node.right is not None:
            stack.append((node.right, node.val, upper))
        if node.left is not None:
            stack.append((node.left, lower, node.val))
    return True


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(is_valid_bst(root))
    print(is_valid_bst_iterative(root))


if __name__ == "__main__":
    main()
