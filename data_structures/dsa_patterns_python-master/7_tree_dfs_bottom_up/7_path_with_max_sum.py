"""Maximum-sum nonempty path between any two nodes (124).

Time: O(n); space: O(h). Empty trees return 0."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.max_sum = float('-inf')


def find_maximum_path_sum(root):
    if root is None:
        return 0
    result = Result()

    def dfs(node):
        left_gain = right_gain = 0
        if node.left is not None:
            left_gain = max(0, dfs(node.left))
        if node.right is not None:
            right_gain = max(0, dfs(node.right))
        result.max_sum = max(result.max_sum, node.val + left_gain + right_gain)
        # Only one branch may extend upward to the parent.
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return result.max_sum


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_maximum_path_sum(root))


if __name__ == "__main__":
    main()
