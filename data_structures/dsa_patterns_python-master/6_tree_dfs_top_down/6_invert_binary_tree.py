"""Invert a binary tree in place (226). Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root):
    if root is None:
        return None

    def dfs(node):
        if node.left is None and node.right is None:
            return
        node.left, node.right = node.right, node.left
        if node.left is not None:
            dfs(node.left)
        if node.right is not None:
            dfs(node.right)

    dfs(root)
    return root


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    invert_tree(root)
    print(root.left.val, root.right.val)


if __name__ == "__main__":
    main()
