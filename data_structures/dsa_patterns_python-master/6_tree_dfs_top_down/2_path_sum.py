"""Root-to-leaf path sum (112). Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def has_path(root, target):
    if root is None:
        return False
    flag = [False]

    def dfs(node, remaining):
        remaining -= node.val
        if node.left is None and node.right is None:
            if remaining == 0:
                flag[0] = True
        if node.left is not None:
            dfs(node.left, remaining)
        if node.right is not None:
            dfs(node.right, remaining)

    dfs(root, target)
    return flag[0]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(has_path(root, 7))


if __name__ == "__main__":
    main()
