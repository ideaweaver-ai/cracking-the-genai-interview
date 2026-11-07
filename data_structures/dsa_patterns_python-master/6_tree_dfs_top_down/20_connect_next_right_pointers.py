"""Populate next-right pointers (116).

Requires a perfect binary tree. Time: O(n); stack: O(h).
Mutates next pointers and returns the original root."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = None


def connect(root):
    if root is None:
        return None

    def dfs(node, parent):
        if parent is None:
            node.next = None
        elif node is parent.left and parent.right is not None:
            node.next = parent.right
        else:
            node.next = parent.next.left if parent.next is not None else None
        if node.left is None and node.right is None:
            return
        if node.left is not None:
            dfs(node.left, node)
        if node.right is not None:
            dfs(node.right, node)

    dfs(root, None)
    return root


def main():
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    connect(root)
    print(root.left.next.val, root.right.next)


if __name__ == "__main__":
    main()
