"""N-ary tree height in edges. Time: O(n); space: O(h).

A leaf has height 0; an empty tree also returns 0 by convention."""


class TreeNode:
    def __init__(self, val, children=None):
        self.val = val
        self.children = [] if children is None else children


def find_height(root):
    if root is None:
        return 0

    def dfs(node):
        if not node.children:
            return 0
        height = 0
        for child in node.children:
            height = max(height, 1 + dfs(child))
        return height

    return dfs(root)


def main():
    root = TreeNode(1, [TreeNode(2, [TreeNode(4)]), TreeNode(3)])
    print(find_height(root))


if __name__ == "__main__":
    main()
