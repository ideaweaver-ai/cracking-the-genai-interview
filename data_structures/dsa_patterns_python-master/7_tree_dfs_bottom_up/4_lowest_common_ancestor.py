"""Lowest common ancestor by node identity (236).

Returns None if either node is absent. Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.ancestor = None


def lowest_common_ancestor(root, p, q):
    if root is None:
        return None
    result = Result()

    def dfs(node):
        p_found = node is p
        q_found = node is q
        if node.left is not None:
            left_p, left_q = dfs(node.left)
            p_found = p_found or left_p
            q_found = q_found or left_q
        if node.right is not None:
            right_p, right_q = dfs(node.right)
            p_found = p_found or right_p
            q_found = q_found or right_q
        if p_found and q_found and result.ancestor is None:
            result.ancestor = node
        return p_found, q_found

    dfs(root)
    return result.ancestor


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(lowest_common_ancestor(root, root.left.left, root.left.right).val)


if __name__ == "__main__":
    main()
