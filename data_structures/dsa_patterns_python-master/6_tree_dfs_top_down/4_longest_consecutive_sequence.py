"""Longest increasing parent-to-child consecutive sequence (298).

Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def longest_consecutive(root):
    if root is None:
        return 0
    global_max = [0]

    def dfs(node, parent_value, length):
        length = length + 1 if node.val == parent_value + 1 else 1
        global_max[0] = max(global_max[0], length)
        if node.left is None and node.right is None:
            return
        if node.left is not None:
            dfs(node.left, node.val, length)
        if node.right is not None:
            dfs(node.right, node.val, length)

    dfs(root, root.val, 0)
    return global_max[0]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(longest_consecutive(root))


if __name__ == "__main__":
    main()
