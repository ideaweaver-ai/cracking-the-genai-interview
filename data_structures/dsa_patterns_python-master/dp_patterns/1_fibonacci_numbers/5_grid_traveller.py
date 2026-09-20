# Time: O(m*n) | Space: O(m+n)

class Solution:
    # Time: O(m*n) | Space: O(m+n)
    # def uniquePaths(self, m: int, n: int, memo = {}) -> int:
    #     # base cases
    #     if m == 0 or n == 0:
    #         return 0
    #     if m == 1 and n == 1:
    #         return 1
    #     # memoization
    #     if (m, n) in memo:
    #         return memo[(m,n)]
    #     # recursion
    #     memo[(m, n)] = self.uniquePaths(m-1, n, memo) + self.uniquePaths(m, n-1, memo)
    #     return memo[(m, n)]

    # Time: O(m*n) | Space: O(m+n)
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        # base cases
        #         for i in range(n):
        #             dp[0][i] = 0

        #         for i in range(m):
        #             dp[i][0] = 0

        dp[1][1] = 1

        # recursion
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # so we dont owerwrite the base case
                if i == 1 and j == 1:
                    continue
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m][n]
