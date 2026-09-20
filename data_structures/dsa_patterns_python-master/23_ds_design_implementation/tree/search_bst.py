from tree.bst_print import TreeNode


# Iterative
# O(log(N)) time | O(1) space
def search_iterative(current_node, key):
    if current_node is None:
        return False
    while current_node:
        if key == current_node.val:
            return True
        elif key < current_node.val:
            current_node = current_node.left
        else:
            current_node = current_node.right
    return False


# Recursive
# O(log(N)) time | O(log(N)) space
def search_recursive(current_node, key):
    # base cases
    if current_node is None:
        return False
    if key == current_node.val:
        return True
    # recursive calls
    elif key <= current_node.val:
        return search_recursive(current_node.left, key)
    else:
        return search_recursive(current_node.right, key)


if __name__ == '__main__':
    # Build Tree for testing
    root = TreeNode(20)
    root.left = TreeNode(10)
    root.right = TreeNode(40)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(15)
    root.right.left = TreeNode(30)
    root.right.right = TreeNode(50)
    root.display()
    key1, key2 = 5, 14
    print(f'Search {key1}: {search_iterative(root, key1)}')
    print(f'Search {key2}: {search_iterative(root, key2)}')
    print(f'Search {key1}: {search_recursive(root, key1)}')
    print(f'Search {key2}: {search_iterative(root, key2)}')