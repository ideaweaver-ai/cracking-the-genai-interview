"""Print all root-to-leaf paths using DFS.

Time: O(n + output size); auxiliary space: O(h), excluding returned paths."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_paths(root):
    if root is None:
        return []
    result = []

    def dfs(node, slate):
        slate.append(node.val)
        # Base case: leaf node. Save a copy before backtracking.
        if node.left is None and node.right is None:
            result.append(slate[:])
        # Recursive case: internal node.
        if node.left is not None:
            dfs(node.left, slate)
        if node.right is not None:
            dfs(node.right, slate)
        slate.pop()

    dfs(root, [])
    return result


def print_paths(root):
    for path in find_paths(root):
        print(*path)


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print_paths(root)


if __name__ == "__main__":
    main()
