from tree.bst_print import TreeNode


def findKNodes(root, k):
    def helper(root, depth):
        if root is None:
            return
        if depth == k:
            result.append(root.val)
        # recursive calls
        helper(root.left, depth + 1)
        helper(root.right, depth + 1)

    result = []
    helper(root, 0)
    return result


# Add test case - python-ds- refresher