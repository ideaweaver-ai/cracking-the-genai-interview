"""Level-order traversal using top-down DFS (LeetCode 102).

Time: O(n). Auxiliary stack space: O(h), excluding the O(n) output.
"""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def traverse(root):
    if root is None:
        return []

    result = []

    def dfs(node, level):
        # Process current node.
        if level == len(result):
            result.append([])
        result[level].append(node.val)

        # Base case: leaf node.
        if node.left is None and node.right is None:
            return

        # Recursive case: pass the next level to each child.
        if node.left is not None:
            dfs(node.left, level + 1)
        if node.right is not None:
            dfs(node.right, level + 1)

    dfs(root, 0)
    return result


def main():
    root = TreeNode(
        1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3, TreeNode(6), TreeNode(7)),
    )
    print(traverse(root))
    # [[1], [2, 3], [4, 5, 6, 7]]


if __name__ == "__main__":
    main()
