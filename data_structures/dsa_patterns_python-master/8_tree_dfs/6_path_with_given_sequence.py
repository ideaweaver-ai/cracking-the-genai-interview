# Copyright © 2020 way2FAANG

# LeetCode: 1430


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_path(root, sequence):
    return find_path_helper(root, sequence, [])


# Time
# Worst case - Balanced tree
# Traverse all nodes = O(N) + N/2 leaves. Potentially each leaf is result. compare current path with seq = O(n/2*log(N))
# Total = O(n) + O(N*log(N)) = O(N*log(N))
# Space
# Worst case -Tree is linked list
# O(N) for stack and current_path
def find_path_helper(current_node, sequence, current_path):
    # 1) base case 1
    # Case where parent node has only 1 child and we end with a call to None
    if current_node is None:
        return False

    # 2) process current node - include current node in current path
    current_path.append(current_node.val)
    if current_node.left is None and current_node.right is None:
        # 3) base case 2
        # vimp not to return here because we need to backtrack
        result = (current_path == sequence)  # O(m)
    else:
        # 4) Recursive calls
        # Cant return here, we need to backtrack here
        result = find_path_helper(current_node.left, sequence, current_path) or find_path_helper(current_node.right,
                                                                                                 sequence, current_path)
        # Imp to backtrack before result
    del current_path[-1]
    return result


# Can we do better ? Yes
# Time:
# O(n) every node visited once
# Space:
# O(n) stack space - worst case linked list structure
def find_path(root, sequence):
    # Validate input
    if not root:
        return len(sequence) == 0
    return find_path_helper(root, sequence, 0)


def find_path_helper(current_node, sequence, sequence_index):
    # 1) base case 1
    # Case where parent node has only 1 child and we end with a call to None
    if current_node is None:
        return False

    # 2) process current node - include current node in current path
    # Very imp to check sequence_index >= len(sequence) -
    # case where sequence is smaller than tree, else it will give Null pointer
    # Generally when dealing with array index in recursion, check index out of bound
    if sequence_index >= len(sequence) or current_node.val != sequence[sequence_index]:
        return False

    # 3) base case 2
    if current_node.left is None and current_node.right is None and sequence_index == len(sequence) - 1:
        return True

    # 4) Recursive calls
    result = find_path_helper(current_node.left, sequence, sequence_index + 1) or find_path_helper(current_node.right,
                                                                                                   sequence,
                                                                                                   sequence_index + 1)

    return result


def main():
    root = TreeNode(1)
    root.left = TreeNode(0)
    root.right = TreeNode(1)
    root.left.left = TreeNode(1)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(5)

    print("Tree has path sequence: " + str(find_path(root, [1, 0, 7])))
    print("Tree has path sequence: " + str(find_path(root, [1, 1, 6])))


main()
