"""Turn a binary tree upside down in place (156).

Precondition: every right child is a leaf with a left sibling, or absent.
Time: O(h); stack: O(h). Only the left spine needs visiting."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def upside_down_tree(root):
    if root is None:
        return None
    new_root = [None]

    def dfs(node, parent, right_sibling):
        old_left, old_right = node.left, node.right
        node.left = right_sibling
        node.right = parent
        if old_left is None:
            new_root[0] = node
            return
        dfs(old_left, node, old_right)

    dfs(root, None, None)
    return new_root[0]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    root = upside_down_tree(root)
    print(root.val, root.left.val, root.right.val)


if __name__ == "__main__":
    main()
