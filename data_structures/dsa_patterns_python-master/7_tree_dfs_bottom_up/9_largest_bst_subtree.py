"""Size of the largest strict BST subtree (333).

A subtree includes all descendants. Duplicate values are invalid in a BST.
Time: O(n); stack: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.max_size = 0


def largest_bst_subtree(root):
    if root is None:
        return 0
    result = Result()

    def dfs(node):
        size = 1
        smallest = largest = node.val
        valid = True
        if node.left is not None:
            child_size, child_min, child_max, child_valid = dfs(node.left)
            size += child_size
            smallest = min(smallest, child_min)
            largest = max(largest, child_max)
            if not child_valid or child_max >= node.val:
                valid = False
        if node.right is not None:
            child_size, child_min, child_max, child_valid = dfs(node.right)
            size += child_size
            smallest = min(smallest, child_min)
            largest = max(largest, child_max)
            if not child_valid or child_min <= node.val:
                valid = False
        if valid:
            result.max_size = max(result.max_size, size)
        return size, smallest, largest, valid

    dfs(root)
    return result.max_size


def main():
    root = TreeNode(10, TreeNode(5, TreeNode(1), TreeNode(8)),
                    TreeNode(15, right=TreeNode(7)))
    print(largest_bst_subtree(root))


if __name__ == "__main__":
    main()
