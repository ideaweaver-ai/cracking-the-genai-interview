"""N-ary maximum depth in nodes and height in edges (559).

Time: O(n); space: O(h). Empty trees return 0 for either convention."""


class TreeNode:
    def __init__(self, val, children=None):
        self.val = val
        self.children = [] if children is None else children


def max_depth(root):
    return _height(root, 0)


def find_height(root):
    return _height(root, -1)


def _height(root, initial_depth):
    if root is None:
        return 0
    global_height = [0]

    def dfs(node, depth_to_parent):
        depth = depth_to_parent + 1
        global_height[0] = max(global_height[0], depth)
        if not node.children:
            return
        for child in node.children:
            dfs(child, depth)

    dfs(root, initial_depth)
    return global_height[0]


def main():
    root = TreeNode(1, [TreeNode(2, [TreeNode(4)]), TreeNode(3)])
    print(max_depth(root), find_height(root))


if __name__ == "__main__":
    main()
