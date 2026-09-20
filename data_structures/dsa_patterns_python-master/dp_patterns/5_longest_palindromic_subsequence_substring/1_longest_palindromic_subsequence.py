# Time: O(n*2**n) | Space: O(n)
# def find_LPS_length(st):
#     def find_LPS_length_helper(subseq, i):
#         # base cases
#         if i == n:
#             if find_palindrome(subseq):
#                 return len(subseq)
#             else:
#                 return 0
#         # recursion calls
#         # case 1 - i included in subsequence
#         subseq.append(st[i])
#         l1 = find_LPS_length_helper(subseq, i + 1)
#         del subseq[-1]
#         # case 1 - i not included in subsequence
#         l2 = find_LPS_length_helper(subseq, i + 1)
#         return max(l1, l2)
#
#     # main function
#     n = len(st)
#     return find_LPS_length_helper([], 0)
#
#
# def find_palindrome(subseq):
#     for i in range((len(subseq) + 1) // 2):
#         if subseq[i] != subseq[~i]:
#             return False
#     return True


# Better solution - O(2**n)
# Recursion
# Time: O(2**n) | Space: O(n)
def find_LPS_length(st):
    def find_LPS_length_helper(start, end):
        # base cases
        if start > end:
            return 0

        if start == end:
            return 1

        # recursive calls
        if st[start] == st[end]:
            # we can return becasue this is the best case scenario at this point
            # we can never have a longer palindromic sequence than this
            return 2 + find_LPS_length_helper(start + 1, end - 1)

        # remaining recursive calls
        # we can either move the start or the end
        l1 = find_LPS_length_helper(start + 1, end)
        l2 = find_LPS_length_helper(start, end - 1)

        return max(l1, l2)

    # main function
    return find_LPS_length_helper(0, len(st) - 1)


# Memoized
# Time: O(n**2) | Space: O(n**2)
def find_LPS_length(st):
    def find_LPS_length_helper(start, end):
        # base cases
        if start > end:
            return 0

        if start == end:
            return 1

        # check in memo
        if (start, end) in memo:
            return memo[(start, end)]

        # recursive calls
        if st[start] == st[end]:
            # we can return becasue this is the best case scenario at this point
            # we can never have a longer palindromic sequence than this
            return 2 + find_LPS_length_helper(start + 1, end - 1)

        # remaining recursive calls
        # we can either move the start or the end
        l1 = find_LPS_length_helper(start + 1, end)
        l2 = find_LPS_length_helper(start, end - 1)

        memo[(start, end)] = max(l1, l2)

        return memo[(start, end)]

    # main function
    memo = {}
    return find_LPS_length_helper(0, len(st) - 1)


# Top down DP - better to write code this way
# Time: O(n**2) | Space: O(n**2)
def find_LPS_length(st):
    n = len(st)
    dp = [[0 for _ in range(n)] for _ in range(n + 1)]

    # base cases:
    for i in range(n):
        dp[i][i] = 1

    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n):  # imp - only when end > start, we have valid scenarios
            # recursive calls
            if st[start] == st[end]:
                dp[start][end] = 2 + dp[start + 1][end - 1]
            else:
                l1 = dp[start + 1][end]
                l2 = dp[start][end - 1]
                dp[start][end] = max(l1, l2)

    return dp[0][n - 1]


# Top down optimized DP
# Time: O(n**2) | Space: O(n)
def find_LPS_length(st):
    n = len(st)
    dp = [[0 for _ in range(n)] for _ in range(2)]

    # base cases:
    # since base cases are spread all over the matrix - better to handle all of them in the same loop
    # start greater than end already handled (init tot 0)

    for start in range(n - 1, -1, -1):
        for end in range(1, n):
            # handle base cases here
            # base case 1
            if start > end:
                dp[start % 2][end] = 0
            # base case 2
            elif start == end:
                dp[start % 2][end] = 1
            # recursive calls
            elif st[start] == st[end]:
                dp[start % 2][end] = 2 + dp[(start + 1) % 2][end - 1]
            else:
                l1 = dp[(start + 1) % 2][end]
                l2 = dp[start % 2][end - 1]
                dp[start % 2][end] = max(l1, l2)

    return dp[0][n - 1]


def main():
    print(find_LPS_length("abdbca"))
    print(find_LPS_length("cddpd"))
    print(find_LPS_length("pqr"))


main()
