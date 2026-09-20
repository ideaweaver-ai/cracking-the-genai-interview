# Copyright © 2020 way2FAANG


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_sum_of_path_numbers(root):
    # since result is int (immutable) we will return from helper not pass as parameter
    return find_sum_of_path_numbers_helper(root, 0)


# Time - O(N) as every node is visited once
# Space:
# Worst case - O(N) when tree is Linked list
def find_sum_of_path_numbers_helper(current_node, current_sum):
    # Imp base case - Don't miss.
    # E.g. when node has only 1 child say left, after calculating left_sum, we will call helper function on right child
    # But right child will be None. So that will give a Null pointer exception
    # base case 1
    if current_node is None:
        return 0

    # Process current node first
    # multiply current_sum by 10 and add current node val
    current_sum *= 10
    current_sum += current_node.val

    # base case 2
    # Imp to return at leaf node, instead of empty. If we return at empty node we will double the sum
    if current_node.left is None and current_node.right is None:
        return current_sum

    # Think at high level - when at a node
    # Add sum of all leaf paths in left branch and right branch and return
    return find_sum_of_path_numbers_helper(current_node.left, current_sum) + find_sum_of_path_numbers_helper(current_node.right, current_sum)
    # No need to backtrack as we are passing immutables
    # ** Remember: We need to return - since result is immutable and not modified as referenced parameter


def main():
    root = TreeNode(1)
    root.left = TreeNode(0)
    root.right = TreeNode(1)
    root.left.left = TreeNode(1)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(5)
    print("Total Sum of Path Numbers: " + str(find_sum_of_path_numbers(root)))


main()
