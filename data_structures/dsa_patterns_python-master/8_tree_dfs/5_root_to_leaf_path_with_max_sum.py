# Copyright © 2020 way2FAANG


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_max_path(root):
    result = [None]
    max_sum = [-float('inf')]
    helper(root, [], result, max_sum, 0)
    return max_sum[0], result

# simpler version without backtracking
# def helper(currentNode, currentPath, result, maxSum, currentSum):
#     """return result and maxSum, since maxSum is int
#     Ideally is better to backtrack with currentSum. This example just shows hw to do it without backtracking, but increases TC"""
#     if currentNode is None:
#         return maxSum, result
#     # Need to use currentSum var instead of doing sum of currentPath.
#     # Else it will increase time complexity. TC multiplied ny O(log(N))
#     currentSum += currentNode.val
#
#
#     # Code could be simplified
#     if currentNode.left is None and currentNode.right is None:
#         if currentSum > maxSum:
#             maxSum = currentSum
#             result = currentPath + [currentNode.val]  # increases time comp. but prevents backtracking
#
#     maxSumLeft, resultLeft = helper3(currentNode.left, currentPath + [currentNode.val], result, maxSum, currentSum)
#     maxSumRight, resultRight = helper3(currentNode.right, currentPath + [currentNode.val], result, maxSum, currentSum)
#     if maxSumLeft > maxSumRight:
#         return maxSumLeft, resultLeft
#     else:
#         return maxSumRight, resultRight


def helper(current_node, current_path, result, max_sum, current_sum):
    """update current_path, result and max_sum(as list) and backtrack current_path
    When we are solving this way without returning anything from helper we need to pass maxSuma in a list
     Becuase if we pass as an int - imagine 1 recursive call where max_sum is coming as an int parameter.
     Then we process current_node and call helper on left node. If we get a new max in the call to the leftNode the call
     to right node will not pass this new max as int parameter as int is immutable, instead it will pass max_sum parameter
     received as parameter in the parent node call"""
    if current_node is None:
        return

    # process  current node
    current_path.append(current_node.val)
    current_sum += current_node.val

    # base case 2
    if current_node.left is None and current_node.right is None and current_sum > max_sum[0]:
        # print("updating result")
        # print(current_path)
        # print(max_sum)

        result[0] = list(current_path)  # v imp update - dont create new list
        max_sum[0] = current_sum  # v imp update - dont create new list
        # print(result)
        # print(max_sum)
    else:
        helper(current_node.left, current_path, result, max_sum, current_sum)
        helper(current_node.right, current_path, result, max_sum, current_sum)
    del current_path[-1]
    # No need to update current_sum as it is not passed by reference


def find_max_path2(root):
    max_sum = helper2(root, [], [], -float('inf'), 0)
    return max_sum


def helper2(current_node, current_path, result, max_sum, current_sum):
    """return result and max_sum, since max_sum is int"""
    # 1) base case 1
    if current_node is None:
        return max_sum, result

    # 2) process current node - include current node in current path and add val to current sum
    # Need to use current_sum var instead of doing sum of current_path.
    # Else it will increase time complexity. TC multiplied ny O(log(N))
    current_sum += current_node.val
    current_path.append(current_node.val)

    # 3) base case 2
    if current_node.left is None and current_node.right is None and current_sum > max_sum:
        max_sum = current_sum
        result = list(current_path)

    max_sum_left, result_left = helper2(current_node.left, current_path, result, max_sum, current_sum)
    max_sum_right, result_right = helper2(current_node.right, current_path, result, max_sum, current_sum)

    # back track
    del current_path[-1]

    if max_sum_left > max_sum_right:
        return max_sum_left, result_left
    else:
        return max_sum_right, result_right


def find_max_path3(root):
    result = [None]
    max_sum = helper3(root, [], result, -float('inf'), 0)
    return max_sum, result


def helper3(current_node, current_path, result, max_sum, current_sum):
    """return result and max_sum, since max_sum is int
    Ideally is better to backtrack with current_sum. This example just shows hw to do it without backtracking, but increases TC"""
    if current_node is None:
        return max_sum
    # Need to use current_sum var instead of doing sum of current_path.
    # Else it will increase time complexity. TC multiplied ny O(log(N))
    current_path.append(current_node.val)
    current_sum += current_node.val

    # Code could be simplified
    if current_node.left is None and current_node.right is None and current_sum > max_sum:
            max_sum = current_sum
            result[0] = list(current_path)

    max_sum_left = helper3(current_node.left, current_path, result, max_sum, current_sum)
    max_sum_right = helper3(current_node.right, current_path, result, max_sum, current_sum)

    del current_path[-1]

    return max(max_sum_left, max_sum_right)


# best way
# TC: O(n*log(n)) | Space : O(log(N))
class Solution:
    def __init__(self):
        self.max_path_sum = -float('inf')
        self.max_path = None

    def find_max_sum_path(self, root):
        self.find_max_sum_path_helper(root, 0, [])
        return self.max_path_sum, self.max_path

    def find_max_sum_path_helper(self, current_node, path_sum, current_path):
        # base case 1
        if current_node is None:
            return

        # process current_node
        current_path.append(current_node.val)
        path_sum += current_node.val

        # base case 2 -leaf node
        if current_node.left is None and current_node.right is None:
            if path_sum > self.max_path_sum:
                self.max_path_sum = path_sum
                self.max_path = list(current_path)

        # recursion
        self.find_max_sum_path_helper(current_node.left, path_sum, current_path)
        self.find_max_sum_path_helper(current_node.right, path_sum, current_path)

        # backtrack --only current path
        del current_path[-1]


def main():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    print(f"Max sum to leaf paths is {find_max_path3(root)[0]} : {find_max_path3(root)[1]}")
    sol = Solution()
    print(f"Max sum to leaf paths is {sol.find_max_sum_path(root)[0]} : {sol.find_max_sum_path(root)[1]}")


main()
