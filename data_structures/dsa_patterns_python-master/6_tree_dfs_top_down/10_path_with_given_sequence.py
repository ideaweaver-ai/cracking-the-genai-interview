"""Match an entire root-to-leaf sequence (1430). Time: O(n); space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_path(root, sequence):
    if root is None:
        return len(sequence) == 0
    found = [False]

    def dfs(node, index):
        if index >= len(sequence) or node.val != sequence[index]:
            return
        if node.left is None and node.right is None:
            if index == len(sequence) - 1:
                found[0] = True
            return
        if node.left is not None:
            dfs(node.left, index + 1)
        if node.right is not None:
            dfs(node.right, index + 1)

    dfs(root, 0)
    return found[0]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_path(root, [1, 2, 4]))


if __name__ == "__main__":
    main()
