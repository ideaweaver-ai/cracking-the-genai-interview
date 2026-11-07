"""All root-to-leaf paths with a target sum (113).

Time: O(n + output size); auxiliary space: O(h)."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_paths(root, target):
    if root is None:
        return []
    result = []

    def dfs(node, slate, remaining):
        slate.append(node.val)
        remaining -= node.val
        if node.left is None and node.right is None:
            if remaining == 0:
                result.append(slate[:])
        if node.left is not None:
            dfs(node.left, slate, remaining)
        if node.right is not None:
            dfs(node.right, slate, remaining)
        slate.pop()

    dfs(root, [], target)
    return result


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print(find_paths(root, 7))


if __name__ == "__main__":
    main()
