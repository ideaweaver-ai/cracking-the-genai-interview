"""Print all root-to-leaf paths using BFS.

Time: O(n*h); auxiliary space: O(w*h) for queued path copies."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


from collections import deque


def find_paths(root):
    if root is None:
        return []
    result = []
    queue = deque([(root, [])])
    while queue:
        node, slate = queue.popleft()
        slate = slate + [node.val]
        if node.left is None and node.right is None:
            result.append(slate)
            continue
        if node.left is not None:
            queue.append((node.left, slate))
        if node.right is not None:
            queue.append((node.right, slate))
    return result


def print_paths(root):
    for path in find_paths(root):
        print(*path)


def main():
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    print_paths(root)


if __name__ == "__main__":
    main()
