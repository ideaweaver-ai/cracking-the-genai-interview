# Copyright © 2020 way2FAANG

# LeetCode: 124

import math


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Time: O(N) time every node visited once | Space: worst case - linked list - O(N)
def find_maximum_path_sum(root):
    max_path_sum = MaximumPathSum()
    max_path_sum.find_maximum_path_sum_helper(root)
    return max_path_sum.global_max_sum


class MaximumPathSum:
    def __init__(self):
        self.global_max_sum = -math.inf

    def find_maximum_path_sum_helper(self, current_node):
        # 1) base case
        if current_node is None:
            return 0

        # 2) & 3) process current node and recursive calls
        max_path_sum_from_left = self.find_maximum_path_sum_helper(current_node.left)
        max_path_sum_from_right = self.find_maximum_path_sum_helper(current_node.right)

        # ** imp - ignore paths with negative sums, since we need to find the maximum sum we should
        # ignore any path which has an overall negative sum.
        max_path_sum_from_left = max(max_path_sum_from_left, 0)
        max_path_sum_from_right = max(max_path_sum_from_right, 0)

        # maximum path sum at the current node will be equal to the sum from the left subtree +
        # the sum from right subtree + val of current node
        local_max_sum = max_path_sum_from_left + max_path_sum_from_right + current_node.val

        # ** imp - update the global maximum sum
        self.global_max_sum = max(self.global_max_sum, local_max_sum)

        # 4) return since max sum at any node is immutable
        # maximum sum of any path from the current node will be equal to the maximum of
        # the sums from left or right subtrees plus the value of the current node
        # since path can be between any nodes - (1 of the nodes need not be leaf node)
        return max(max_path_sum_from_left, max_path_sum_from_right) + current_node.val


def main():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)

    print("Maximum Path Sum: " + str(find_maximum_path_sum(root)))
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(6)
    root.right.left.left = TreeNode(7)
    root.right.left.right = TreeNode(8)
    root.right.right.left = TreeNode(9)
    print("Maximum Path Sum: " + str(find_maximum_path_sum(root)))

    root = TreeNode(-1)
    root.left = TreeNode(-3)
    print("Maximum Path Sum: " + str(find_maximum_path_sum(root)))


main()
