from tree.bst_print import TreeNode


def findMin(root):
    while root.left:
        root = root.left
    return root


# Recursive - Delete node is simpler recursively. Iteratively can be done but complicated
def deleteNode(root, key):
    # Base Case
    if root is None:
        return root

    # Go left
    if key < root.val:
        root.left = deleteNode(root.left, key)  # imp - after deleting to pass reference to parent

    elif key > root.val:
        root.right = deleteNode(root.right, key)  # imp - after deleting to pass reference to parent

    else:
        # Node to be deleted found

        # Node has one one or two children
        if root.left is None:
            return root.right  # since incoming reference to node to be deleted is lost it will be garbage collected

        # Node has one one or two children
        elif root.right is None:
            return root.left  # since incoming reference to node to be deleted is lost it will be garbage collected

        # Two children
        else:
            # find inorder successor or predecessor
            # We will find inorder successor
            successor = findMin(root.right)
            # replace current node with successor
            root.val = successor.val

            # delete the successor
            root.right = deleteNode(root.right, successor.val)  # as root value changed to successor, don't delete from successor, it will cause error

    return root  # vv imp for this to work we need to return the current node up through the recursive calls


if __name__ == '__main__':
    # Build Tree for testing
    root = TreeNode(20)
    root.left = TreeNode(10)
    root.right = TreeNode(40)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(15)
    root.right.left = TreeNode(30)
    root.right.right = TreeNode(50)
    root.right.right.right = TreeNode(60)
    root.right.right.right.right = TreeNode(80)
    print("Before")
    root.display()
    deleteNode(root, 10)
    print()
    print("After deleting 10")
    root.display()
    deleteNode(root, 80)
    print()
    print("After deleting 80")
    root.display()

    deleteNode(root, 100)
    print()
    print("After deleting 100")
    root.display()
