# Time: O(n * 2**n) | Space: O(2**n) - for stack

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# since we need only count we can simplify them again
# def count_trees(n):
#     total_trees = 0
#
#     if n <= 1:
#         return 1
#
#     for i in range(1, n + 1):
#         count_left = count_trees(i - 1)
#         count_right = count_trees(n - i)
#         total_trees += (count_left * count_right)
#     return total_trees


# memoized version
# Time: O(n) | Space: O(n)
def count_trees(n):
    memo = {}
    count = count_trees_helper(n, memo)
    return count


def count_trees_helper(n, memo):
    if n in memo:
        return memo[n]

    total_trees = 0

    if n <= 1:
        return 1

    for i in range(1, n + 1):
        count_left = count_trees_helper(i - 1, memo)
        count_right = count_trees_helper(n - i, memo)
        total_trees += (count_left * count_right)

    memo[n] = total_trees
    return total_trees




def main():
    print("Total trees: " + str(count_trees(2)))
    print("Total trees: " + str(count_trees(3)))


main()
