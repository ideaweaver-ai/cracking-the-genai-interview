"""N-ary maximum depth in nodes and height in edges (559).

Time: O(n); space: O(h). Empty trees return 0 for either convention."""


class TreeNode:
    def __init__(self, val, children=None):
        self.val = val
        self.children = [] if children is None else children


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.max_height = 0


def max_depth(root):
    return _height(root, 0)


def find_height(root):
    return _height(root, -1)


def _height(root, initial_depth):
    if root is None:
        return 0
    result = Result()

    def dfs(node, depth_to_parent):
        depth = depth_to_parent + 1
        result.max_height = max(result.max_height, depth)
        if not node.children:
            return
        for child in node.children:
            dfs(child, depth)

    dfs(root, initial_depth)
    return result.max_height


def main():
    root = TreeNode(1, [TreeNode(2, [TreeNode(4)]), TreeNode(3)])
    print(max_depth(root), find_height(root))


if __name__ == "__main__":
    main()
