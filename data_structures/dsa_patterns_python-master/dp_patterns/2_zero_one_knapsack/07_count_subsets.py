# # Recursive (2^n) time | O(n) space
# def count_subsets(num, S):
#     if len(num) == 0 or S == 0:
#         return 0
#     return helper(num, S, 0)
#
#
# def helper(num, S, i):
#     # base case
#     if S == 0:
#         return 1
#     if i == len(num):
#         return 0
#     # Recursion
#     count1, count2 = 0, 0
#     if num[i] <= S:
#         count1 = helper(num, S - num[i], i + 1)
#     count2 = helper(num, S, i + 1)
#     return count1 + count2


# Memoized (n*) time | O(n*s) space
# def count_subsets(num, S):
#     if len(num) == 0 or S == 0:
#         return 0
#     dp = [[-1 for _ in range(S+1)] for _ in range(len(num))]
#     return helper(num, S, 0, dp)
#
#
# def helper(num, S, i, dp):
#     # base case
#     if S == 0:
#         return 1
#     if i == len(num):
#         return 0
#     # check memo
#     if dp[i][S] != -1:
#         return dp[i][S]
#     # Recursion
#     count1, count2 = 0, 0
#     if num[i] <= S:
#         count1 = helper(num, S - num[i], i + 1, dp)
#     count2 = helper(num, S, i + 1, dp)
#     dp[i][S] = count1 + count2
#     return count1 + count2


# Tabulation - O(n*s) time | O(n*s) space
def count_subsets(num, S):
    n = len(num)
    if n == 0 or S == 0:
        return 0
    dp = [[0 for _ in range(S+1)] for _ in range(n+1)]

    # dp base values
    for i in range(n+1):  # v imp in this case [n][0] is also 1- means ith element made sum (remaining) 0 and it was noticed in i+1 iteration
        dp[i][0] = 1

    # dp tabulation
    for i in range(n-1, -1, -1):
        for s in range(1, S+1):
            count1, count2 = 0, 0
            if num[i] <= s:
                count1 = dp[i+1][s-num[i]]
            count2 = dp[i+1][s]
            dp[i][s] = count1 + count2

    return dp[0][S]







def main():
    print("Total number of subsets " + str(count_subsets([1, 1, 2, 3], 4)))
    print("Total number of subsets: " + str(count_subsets([1, 2, 7, 1, 5], 9)))


main()
