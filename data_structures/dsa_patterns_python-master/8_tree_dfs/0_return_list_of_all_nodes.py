class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Recursive
def traverse_recursive(root):
    result = []
    helper(root, result)
    return result


def helper(current_node, result):
    if current_node is None:
        return
    result.append(current_node.val)
    helper(current_node.left, result)
    helper(current_node.right, result)


# Iterative
def traverse_iterative(root):
    result = []
    stack = list()
    stack.append(root)
    while stack:
        current_node = stack.pop()
        result.append(current_node.val)
        # Since stack is LIFO and we want to process left first, append right then left
        if current_node.right:
            stack.append(current_node.right)
        if current_node.left:
            stack.append(current_node.left)
    return result


def main():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    print(traverse_recursive(root))
    print(traverse_iterative(root))


main()
