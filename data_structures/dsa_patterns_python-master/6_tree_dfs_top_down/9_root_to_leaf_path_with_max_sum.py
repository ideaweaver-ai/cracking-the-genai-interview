"""Maximum-sum root-to-leaf path (including negative values).

Time: O(n*h) with best-path copies; auxiliary space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.max_sum = float('-inf')
        self.path = []


def find_max_path(root):
    if root is None:
        return 0, []
    result = Result()

    def dfs(node, path_sum, slate):
        path_sum += node.val
        slate.append(node.val)
        if node.left is None and node.right is None:
            if path_sum > result.max_sum:
                result.max_sum = path_sum
                result.path = slate[:]
        if node.left is not None:
            dfs(node.left, path_sum, slate)
        if node.right is not None:
            dfs(node.right, path_sum, slate)
        slate.pop()

    dfs(root, 0, [])
    return result.max_sum, result.path


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_max_path(root))


if __name__ == "__main__":
    main()
