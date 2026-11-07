"""Same tree (100). Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_same_tree(root1, root2):
    if root1 is None or root2 is None:
        return root1 is root2
    same = [True]

    def dfs(node1, node2):
        if node1.val != node2.val:
            same[0] = False
            return
        # Check structure before recursing, so both DFS inputs are non-null.
        for child1, child2 in ((node1.left, node2.left), (node1.right, node2.right)):
            if (child1 is None) != (child2 is None):
                same[0] = False
            elif child1 is not None:
                dfs(child1, child2)

    dfs(root1, root2)
    return same[0]


def main():
    root = TreeNode(1, TreeNode(2), TreeNode(2))
    print(is_same_tree(root, TreeNode(1, TreeNode(2), TreeNode(2))))


if __name__ == "__main__":
    main()
