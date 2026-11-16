"""Longest increasing parent-to-child consecutive sequence (298).

Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.max_length = 0


def longest_consecutive(root):
    if root is None:
        return 0
    result = Result()

    def dfs(node, parent_value, length):
        length = length + 1 if node.val == parent_value + 1 else 1
        result.max_length = max(result.max_length, length)
        if node.left is None and node.right is None:
            return
        if node.left is not None:
            dfs(node.left, node.val, length)
        if node.right is not None:
            dfs(node.right, node.val, length)

    dfs(root, root.val, 0)
    return result.max_length


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(longest_consecutive(root))


if __name__ == "__main__":
    main()
