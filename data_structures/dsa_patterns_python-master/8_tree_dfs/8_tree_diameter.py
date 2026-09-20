# Copyright © 2020 way2FAANG

# LeetCode: 543


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Diameter is a function of height (not depth - dont confuse)
# diameter at a node = left_subtree height + right subtree_height
# We also want to track a global immutable -
# Note we cannot pass parameter without returning it to track a global immutable var - why?
    # consider case - parent receives gloabl var as parameter and passes it left and right child
    # Suppose left child updates the parameter but right child will not get updated value

# so three options - 1) pass it as a list with 1 element
# 2) use a class and set is a instance/class variable
# 3) pass the parameter and return it every time
# option 2 - is easiest and cleanest


# Time: O(N) time every node visited once | Space: worst case - linked list - O(N)
class TreeDiameter:

    def __init__(self):
        self.treeDiameter = 0

    def find_diameter(self, root):
        # Diameter is left height + right height + 1
        self.find_height(root)
        return self.treeDiameter

    def find_height(self, current_node):
        # 1) base case
        if current_node is None:
            return 0

        # 2) & 3) Process current node & Recursive calls
        # In this case no need to have base case for leaf node
        # we are calc height of two children first and based on that calculating the height of the current_node
        left_height = self.find_height(current_node.left)
        right_height = self.find_height(current_node.right)

        # ** imp - Since we know the left height and right here we can calculate the diameter also here
        diameter_at_current_node = left_height + right_height + 1
        self.treeDiameter = max(diameter_at_current_node, self.treeDiameter)

        # 4) return - since height is immutable
        return max(left_height, right_height) + 1


def main():
    treeDiameter = TreeDiameter()
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(6)
    print("Tree Diameter: " + str(treeDiameter.find_diameter(root)))
    root.left.left = None
    root.right.left.left = TreeNode(7)
    root.right.left.right = TreeNode(8)
    root.right.right.left = TreeNode(9)
    root.right.left.right.left = TreeNode(10)
    root.right.right.left.left = TreeNode(11)
    print("Tree Diameter: " + str(treeDiameter.find_diameter(root)))


main()
