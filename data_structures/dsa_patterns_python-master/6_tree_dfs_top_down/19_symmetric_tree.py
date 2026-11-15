"""Symmetric tree (101). Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.is_same = True


def is_symmetric(root):
    if root is None:
        return True
    result = Result()

    def dfs(node1, node2):
        if node1.val != node2.val:
            result.is_same = False
            return
        # Check structure before recursing, so both DFS inputs are non-null.
        for child1, child2 in ((node1.left, node2.right), (node1.right, node2.left)):
            if (child1 is None) != (child2 is None):
                result.is_same = False
            elif child1 is not None:
                dfs(child1, child2)

    dfs(root, root)
    return result.is_same


def main():
    root = TreeNode(1, TreeNode(2), TreeNode(2))
    print(is_symmetric(root))


if __name__ == "__main__":
    main()
