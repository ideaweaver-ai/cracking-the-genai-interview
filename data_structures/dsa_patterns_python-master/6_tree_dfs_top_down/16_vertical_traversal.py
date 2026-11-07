"""Vertical traversal (987).

Sort values sharing a row and column.
Time: O(n log n); space: O(n)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def vertical_traversal(root):
    if root is None:
        return []
    columns = {}

    def dfs(node, column, depth):
        columns.setdefault(column, {}).setdefault(depth, []).append(node.val)
        if node.left is not None:
            dfs(node.left, column - 1, depth + 1)
        if node.right is not None:
            dfs(node.right, column + 1, depth + 1)

    dfs(root, 0, 0)
    result = []
    for column in sorted(columns):
        values = []
        for depth in sorted(columns[column]):
            values.extend(sorted(columns[column][depth]))
        result.append(values)
    return result


def main():
    root = TreeNode(1, TreeNode(2, right=TreeNode(6)),
                    TreeNode(3, left=TreeNode(5)))
    print(vertical_traversal(root))


if __name__ == "__main__":
    main()
