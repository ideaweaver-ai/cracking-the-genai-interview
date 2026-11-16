"""Match an entire root-to-leaf sequence (1430). Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Result:
    """Shared DFS answer, initialized separately for each public call."""

    def __init__(self):
        self.found = False


def find_path(root, sequence):
    if root is None:
        return len(sequence) == 0
    result = Result()

    def dfs(node, index):
        if index >= len(sequence) or node.val != sequence[index]:
            return
        if node.left is None and node.right is None:
            if index == len(sequence) - 1:
                result.found = True
            return
        if node.left is not None:
            dfs(node.left, index + 1)
        if node.right is not None:
            dfs(node.right, index + 1)

    dfs(root, 0)
    return result.found


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_path(root, [1, 2, 4]))


if __name__ == "__main__":
    main()
