# Copyright © 2020 way2FAANG


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Time
# Best case - Tree is balanced - O(N*log(N))
# Worst case - Tree is linked list - O(n**2)
# Space - excluding result
# Worst case O(N) stack space - Tree is Linked list
def count_paths(root, S):
    return count_paths_helper(root, S, [])


def count_paths_helper(current_node, S, current_path):
    # 1) base case
    if current_node is None:
        return 0
    # 2) Process current node
    current_path.append(current_node)

    # 1 We need to check at every node whether there is a sub path in currrent_path whose sum equals S
    # - as path can be between any two nodes
    # 2 find the sums of all sub-paths in the current path list and check == S
    # 3 easier to go backwards rather than from start to end (figure out why)
    num_paths_with_sum_at_current_node = 0
    current_sum = 0
    for i in range(len(current_path) - 1, -1, -1):
        current_sum += current_path[i].val
        if current_sum == S:
            num_paths_with_sum_at_current_node += 1

    # 3) Recursive calls
    left_count = count_paths_helper(current_node.left, S, current_path)
    right_count = count_paths_helper(current_node.right, S, current_path)

    # 4) Backtrack - since current_path is mutable and modified by reference
    del current_path[-1]

    # 5) return
    return num_paths_with_sum_at_current_node + left_count + right_count


def main():
    root = TreeNode(12)
    root.left = TreeNode(7)
    root.right = TreeNode(1)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(10)
    root.right.right = TreeNode(5)
    print("Tree has paths: " + str(count_paths(root, 11)))


main()
