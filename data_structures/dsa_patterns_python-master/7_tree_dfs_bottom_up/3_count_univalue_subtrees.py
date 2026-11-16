"""Count subtrees whose values are all equal (250).

Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.count = 0


def count_univalue_subtrees(root):
    if root is None:
        return 0
    result = Result()

    def dfs(node):
        if node.left is None and node.right is None:
            result.count += 1
            return True
        is_univalue = True
        if node.left is not None:
            left_univalue = dfs(node.left)
            if not left_univalue or node.left.val != node.val:
                is_univalue = False
        if node.right is not None:
            right_univalue = dfs(node.right)
            if not right_univalue or node.right.val != node.val:
                is_univalue = False
        if is_univalue:
            result.count += 1
        return is_univalue

    dfs(root)
    return result.count


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(count_univalue_subtrees(root))


if __name__ == "__main__":
    main()
