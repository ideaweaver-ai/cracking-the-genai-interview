"""Sum root-to-leaf numbers; node values are digits 0-9 (129).

Time: O(n); space: O(h), assuming constant-time integer arithmetic."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.total = 0


def find_sum_of_path_numbers(root):
    if root is None:
        return 0
    result = Result()

    def dfs(node, number):
        number = number * 10 + node.val
        if node.left is None and node.right is None:
            result.total += number
            return
        if node.left is not None:
            dfs(node.left, number)
        if node.right is not None:
            dfs(node.right, number)

    dfs(root, 0)
    return result.total


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_sum_of_path_numbers(root))


if __name__ == "__main__":
    main()
