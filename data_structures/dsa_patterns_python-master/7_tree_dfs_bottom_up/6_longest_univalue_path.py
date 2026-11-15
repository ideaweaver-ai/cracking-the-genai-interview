"""Longest equal-value path in EDGES (687).

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


def longest_univalue_path(root):
    if root is None:
        return 0
    result = Result()

    def dfs(node):
        if node.left is None and node.right is None:
            return 0
        left_path = right_path = 0
        if node.left is not None:
            length = dfs(node.left)
            if node.left.val == node.val:
                left_path = length + 1
        if node.right is not None:
            length = dfs(node.right)
            if node.right.val == node.val:
                right_path = length + 1
        result.max_length = max(result.max_length, left_path + right_path)
        return max(left_path, right_path)

    dfs(root)
    return result.max_length


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(longest_univalue_path(root))


if __name__ == "__main__":
    main()
