from tree.bst_print import TreeNode


# Iterative
# Worst case - O(n) (Linked List)
# Best case:  O(log(N)) time | O(1) space (Balanced Tree)
# General: O(h) - h is height of tree
def insert_iterative(current_node, key):
    if current_node is None:
        return TreeNode(key)
    while current_node:
        # find node where to insert and store it in previous
        if key <= current_node.val:
            if current_node.left: # left child exists, we can continue looping
                current_node = current_node.left
            else:
                current_node.left = TreeNode(key)
                break
        else:
            if current_node.right:
                current_node = current_node.right
            else:
                current_node.right = TreeNode(key)
                break


# O(log(N)) time | O(log(N)) space
def insert_recursive(current_node, key):
    if current_node is None:
        return TreeNode(key)
    # for this problem its better to combine base cases and recursive calls
    if key <= current_node.val:
        if current_node.left:  # left child exists, recursive call on left child
            insert_recursive(current_node.left, key)
        else:  # left child is None
            current_node.left = TreeNode(key)
    else:
        if current_node.right:  # right child exists, recursive call on right child
            insert_recursive(current_node.right, key)
        else:  # right child is None
            current_node.right = TreeNode(key)


if __name__ == '__main__':
    # Build Tree for testing
    root = TreeNode(20)
    root.left = TreeNode(10)
    root.right = TreeNode(40)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(15)
    root.right.left = TreeNode(30)
    root.right.right = TreeNode(50)
    print("At start")
    root.display()
    print("After inserting 17")
    insert_iterative(root, 17)
    root.display()
    print("After inserting 60")
    insert_recursive(root, 60)
    root.display()
    print("After inserting 29")
    insert_recursive(root, 29)
    root.display()