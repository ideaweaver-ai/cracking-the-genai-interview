# Copyright © 2020 way2FAANG

# LeetCode: 112


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Time: O(n) | Space: O(h) - height of the tree
# Space: O(n) space, Worst case - Tree is a linked list - O(n) time
# Balanced tree - n/2 leaves, Log(n) height - O(N) time visit every node once | O(log(N)) stack space
def has_path(root, sum):
    # In this problem - better to figure out base cases first
    # 1) base case 1
    if root is None:
        return False

    # 2) & 3) process current node and base case 2
    # if current node value is a leaf and its value equals sum (remaining) - we found a path with required sum
    if root.left is None and root.right is None and root.val == sum:
        return True

    # Current inputs are sufficient - so need for helper
    # Recursive call to left and right nodes - Return True if path sum found on either branch
    # Note ** (compare when we have done 0/1 knapsack)
    # In this problem we have to choose the current node and move to it's children,
    # In 0/1 knapsack I can either select or not select the node

    # 4) recursive calls
    # ** imp we can check if left or right child is there and then make recursive call
    # we wouldn't have to check None in base case then
    # problem - this approach will fail when None is passed as root, hence we prefer checking it in the base case
    left_has_path = has_path(root.left, sum - root.val)
    right_has_path = has_path(root.right, sum - root.val)

    # 5) return if required
    return left_has_path or right_has_path


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(9)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    print("Tree has path: " + str(has_path(root, 23)))
    print("Tree has path: " + str(has_path(root, 16)))


main()


