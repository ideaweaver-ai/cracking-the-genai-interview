# Time: O(n * 2**n) | Space: O(2**n)
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def find_unique_trees(n):
    result = find_unique_trees_helper(1, n)
    return result


def find_unique_trees_helper(start, end):
    result = []
    # base cases:
    if start > end:
        return [None]
    for i in range(start, end + 1):
        # making 'i' the root of the tree
        left_subtree_roots = find_unique_trees_helper(start, i - 1)
        right_subtree_roots = find_unique_trees_helper(i + 1, end)
        for left in left_subtree_roots:
            for right in right_subtree_roots:
                root = TreeNode(i)
                root.left = left
                root.right = right
                result.append(root)
    return result
