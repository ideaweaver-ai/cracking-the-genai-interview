"""Maximum-sum root-to-leaf path (including negative values).

Time: O(n*h) with best-path copies; auxiliary space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_max_path(root):
    if root is None:
        return 0, []
    best_sum = [float("-inf")]
    best_path = [[]]

    def dfs(node, path_sum, slate):
        path_sum += node.val
        slate.append(node.val)
        if node.left is None and node.right is None:
            if path_sum > best_sum[0]:
                best_sum[0] = path_sum
                best_path[0] = slate[:]
        if node.left is not None:
            dfs(node.left, path_sum, slate)
        if node.right is not None:
            dfs(node.right, path_sum, slate)
        slate.pop()

    dfs(root, 0, [])
    return best_sum[0], best_path[0]


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_max_path(root))


if __name__ == "__main__":
    main()
