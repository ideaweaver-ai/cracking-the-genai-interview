"""Count downward paths starting and ending anywhere (437).

Time: O(n*h); auxiliary space: O(h). Negative values are supported."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def count_paths(root, target):
    if root is None:
        return 0
    global_count = [0]

    def dfs(node, slate):
        slate.append(node.val)
        suffix_sum = 0
        for value in reversed(slate):
            suffix_sum += value
            if suffix_sum == target:
                global_count[0] += 1
        if node.left is not None:
            dfs(node.left, slate)
        if node.right is not None:
            dfs(node.right, slate)
        slate.pop()

    dfs(root, [])
    return global_count[0]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(count_paths(root, 7))


if __name__ == "__main__":
    main()
