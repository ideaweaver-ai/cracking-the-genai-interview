"""Merge two binary trees (617).

Mutates the first tree; missing branches reuse nodes from the second tree.
Time: O(n + m) upper bound; stack: O(h) for overlapping branches."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def merge_trees(root1, root2):
    if root1 is None:
        return root2
    if root2 is None:
        return root1

    def dfs(node1, node2):
        node1.val += node2.val
        if node1.left is None:
            node1.left = node2.left
        elif node2.left is not None:
            dfs(node1.left, node2.left)
        if node1.right is None:
            node1.right = node2.right
        elif node2.right is not None:
            dfs(node1.right, node2.right)

    dfs(root1, root2)
    return root1


def main():
    root = merge_trees(TreeNode(1, TreeNode(3)), TreeNode(2, right=TreeNode(4)))
    print(root.val, root.left.val, root.right.val)


if __name__ == "__main__":
    main()
