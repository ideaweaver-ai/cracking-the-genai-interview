# Copyright © 2020 way2FAANG

# LeetCode: 257


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_paths(root):
    result = []  # Need to declare a var as we need a reference in this function
    # Similarly, no need for current path var as we don't need it in this function

    # There are two alternatives - 1. include result as path of helper
    # 2. return result in helper. In this we will go with 1
    find_paths_helper(root, result, [])

    return result


# Time
# Worst case - (** When tree is balanced as oppose to Linked List)
# O(n*log(N)) - every node visited once, at each leaf node that matches copy current path to result
# Potentially n/2 leaves, each leaf is end of unique path and have the required sum and added to result
# Hence copy current_path -> height of tree which is log(n)
# Best case - Tree is Linked List
# Every node visited once - O(n), 1 leaf so copy current_Path to result - O(N). total = O(2N) = O(n)

# Space
# Excluding result:
# Worst case - Tree is Linked list
# current_path = O(N), stack space = O(n). Total = O(N)

# Including result
# Worst case - Tree is balanced
# Balanced tree - N/2 leaves, Log(N) height - potentially O(n*log(n)) candidates. So O(Nlog(N))
# Best case - Tree is Linked List
# 1 result candidate of length O(N). So total O(N)
def find_paths_helper(root, result, current_path):
    # 1) base case 1
    if root is None:
        return  # No need to return anything as result as part of helper signature, we are not returning result

    # 2) process current node - include current node in current path
    current_path.append(root.val)

    # 3) base case 2
    # Same logic - current node is leaf and it's value equals remaining sum
    if root.left is None and root.right is None:
        # ** v imp - if we just append current path then it will return empty list ?
        # as current node is removed from current path
        # Generic principle - if appending list (mutalble object) in result append a copy
        # as we need particular state of the mutable object to be part of result and it may be modified in rest of code
        result.append(list(current_path))

        # Don't return as we need to backtrack

    # 4) Recursive calls
    # traverse the left sub-tree
    find_paths_helper(root.left, result, current_path)
    # traverse the right sub-tree
    find_paths_helper(root.right, result, current_path)
    # ** V imp - we need to remove current node from current path - backtrack
    # As we are passing current path by reference in recursive calls
    del current_path[-1]


def main():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    print("All root to leaf paths: {}".format(find_paths(root)))


main()
