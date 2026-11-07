"""Clone a binary tree.

Time: O(n); auxiliary space: O(h), plus O(n) new nodes. No nodes are shared."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def clone_tree(root):
    if root is None:
        return None
    copy = TreeNode(root.val)

    def dfs(node, clone):
        if node.left is not None:
            clone.left = TreeNode(node.left.val)
            dfs(node.left, clone.left)
        if node.right is not None:
            clone.right = TreeNode(node.right.val)
            dfs(node.right, clone.right)

    dfs(root, copy)
    return copy


def main():
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    copy = clone_tree(root)
    print(copy.val, copy.left.val, copy.right.val, copy is root)


if __name__ == "__main__":
    main()
