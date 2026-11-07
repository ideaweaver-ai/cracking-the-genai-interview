"""Find the leftmost value in the deepest row (513).

Time: O(n); space: O(h). Empty trees return None."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_bottom_left_value(root):
    if root is None:
        return None
    leftmost = []

    def dfs(node, depth):
        # Left-first DFS encounters the leftmost node at each depth first.
        if depth == len(leftmost):
            leftmost.append(node.val)
        if node.left is not None:
            dfs(node.left, depth + 1)
        if node.right is not None:
            dfs(node.right, depth + 1)

    dfs(root, 0)
    return leftmost[-1]


def main():
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    print(find_bottom_left_value(root))


if __name__ == "__main__":
    main()
