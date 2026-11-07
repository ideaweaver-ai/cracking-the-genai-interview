"""Preorder traversal, recursive and iterative. Time: O(n); auxiliary space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def traverse_recursive(root):
    if root is None:
        return []
    result = []

    def dfs(node):
        result.append(node.val)
        if node.left is not None:
            dfs(node.left)
        if node.right is not None:
            dfs(node.right)

    dfs(root)
    return result


def traverse_iterative(root):
    if root is None:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(traverse_recursive(root))
    print(traverse_iterative(root))


if __name__ == "__main__":
    main()
