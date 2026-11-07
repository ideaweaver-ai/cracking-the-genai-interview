"""Populate next-right pointers (117).

Works on sparse trees. Time: O(n^2) upper bound due to neighbor scans; stack: O(h).
Mutates next pointers and returns the original root."""


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = None


def connect(root):
    if root is None:
        return None

    def dfs(node, parent):
        if parent is None:
            node.next = None
        elif node is parent.left and parent.right is not None:
            node.next = parent.right
        else:
            neighbor = parent.next
            node.next = None
            while neighbor is not None:
                if neighbor.left is not None:
                    node.next = neighbor.left
                    break
                if neighbor.right is not None:
                    node.next = neighbor.right
                    break
                neighbor = neighbor.next
        if node.left is None and node.right is None:
            return
        # Right first: the next-pointer chain to our right must be ready.
        if node.right is not None:
            dfs(node.right, node)
        if node.left is not None:
            dfs(node.left, node)

    dfs(root, None)
    return root


def main():
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    connect(root)
    print(root.left.next.val, root.right.next)


if __name__ == "__main__":
    main()
