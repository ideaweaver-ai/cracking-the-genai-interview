"""Anticlockwise boundary: root, left boundary, leaves, reversed right boundary (545).

Returns nodes without duplicates. Time: O(n); auxiliary space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_tree_boundary(root):
    if root is None:
        return []
    result = [root]
    right_boundary = []

    def dfs(node, is_left_boundary, is_right_boundary):
        if node.left is None and node.right is None:
            result.append(node)
            return
        if is_left_boundary:
            result.append(node)
        elif is_right_boundary:
            right_boundary.append(node)
        if node.left is not None:
            dfs(node.left, is_left_boundary,
                is_right_boundary and node.right is None)
        if node.right is not None:
            dfs(node.right, is_left_boundary and node.left is None,
                is_right_boundary)

    if root.left is not None:
        dfs(root.left, True, False)
    if root.right is not None:
        dfs(root.right, False, True)
    return result + right_boundary[::-1]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print([node.val for node in find_tree_boundary(root)])


if __name__ == "__main__":
    main()
