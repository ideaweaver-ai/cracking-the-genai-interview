"""Check height balance at every node (110).

Time: O(n); stack: O(h). Empty trees are balanced."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.is_balanced = True


def is_balanced(root):
    if root is None:
        return True
    result = Result()

    def dfs(node):
        # Return height in nodes; a missing child contributes zero.
        if node.left is None and node.right is None:
            return 1
        left_height = right_height = 0
        if node.left is not None:
            left_height = dfs(node.left)
        if node.right is not None:
            right_height = dfs(node.right)
        if abs(left_height - right_height) > 1:
            result.is_balanced = False
        return 1 + max(left_height, right_height)

    dfs(root)
    return result.is_balanced


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    print(is_balanced(root))


if __name__ == "__main__":
    main()
