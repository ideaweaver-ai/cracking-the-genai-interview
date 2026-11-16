"""Binary tree diameter in EDGES (543). Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.diameter = 0


def find_diameter(root):
    if root is None:
        return 0
    result = Result()

    def dfs(node):
        # Return subtree height in edges; missing branches contribute 0.
        if node.left is None and node.right is None:
            return 0
        left_height = right_height = 0
        if node.left is not None:
            left_height = 1 + dfs(node.left)
        if node.right is not None:
            right_height = 1 + dfs(node.right)
        result.diameter = max(result.diameter, left_height + right_height)
        return max(left_height, right_height)

    dfs(root)
    return result.diameter


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_diameter(root))


if __name__ == "__main__":
    main()
