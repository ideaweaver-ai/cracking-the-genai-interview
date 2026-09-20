# Time: (2**(m+n)) | Space: (m)
def solve_rod_cutting(lengths, prices, n):
    def solve_rod_cutting_helper(i, n):
        """Return max profit considering elements from index 0 to i and remaining lenght of rod - n"""
        # base cases
        if n <= 0 or i >= m:  # ideally just == will also do as we are checking n should never become < 0 and i increases by 1 at a time
            return 0

        # recursion calls
        # case 1: cut of 'lenghts[i]' is made
        profit1 = 0
        # we can make a cut of length[i] only if it is <= remaining lenght of rod - n
        if lengths[i] <= n:
            # we can make a cut of lenghts[i] again, so we don't increment the index
            profit1 = prices[i] + solve_rod_cutting_helper(i, n - lengths[i])

        # case 2: cut of 'lenghts[i]' is not made
        profit2 = solve_rod_cutting_helper(i + 1, n)

        return max(profit1, profit2)

    m = len(prices)
    return solve_rod_cutting_helper(0, n)


# Memoized: O(m*n) | Space: O(m*n)
def solve_rod_cutting(lengths, prices, n):
    def solve_rod_cutting_helper(i, n):
        """Return max profit considering elements from index 0 to i and remaining lenght of rod - n"""
        # base cases
        if n <= 0 or i >= m:  # ideally just == will also do as we are checking n should never become < 0 and i increases by 1 at a time
            return 0

        # check in memo
        if memo[i][n] != -1:
            return memo[i][n]

        # recursion calls
        # case 1: cut of 'lenghts[i]' is made
        profit1 = 0
        # we can make a cut of length[i] only if it is <= remaining lenght of rod - n
        if lengths[i] <= n:
            # we can make a cut of lenghts[i] again, so we don't increment the index
            profit1 = prices[i] + solve_rod_cutting_helper(i, n - lengths[i])

        # case 2: cut of 'lenghts[i]' is not made
        profit2 = solve_rod_cutting_helper(i + 1, n)

        # add to memo
        memo[i][n] = max(profit1, profit2)
        return memo[i][n]

    m = len(prices)
    memo = [[-1 for _ in range(n + 1)] for _ in range(m)]
    return solve_rod_cutting_helper(0, n)


# Top down dp
# Time: O(m*n) | Space: O(m*n)
def solve_rod_cutting(lengths, prices, n):
    m = len(prices)

    # init dp
    # top down dp requires one extra row
    dp = [[-1 for _ in range(n + 1)] for _ in range(m + 1)]

    # base cases - look at recursion
    # when remaining rod length (capacity) is 0, profit is 0
    for i in range(m + 1):
        dp[i][0] = 0

    # when i >= m, profit is 0
    for j in range(n):
        dp[m][j] = 0

    # Tabulation
    # go in reverse order of rows
    for i in range(m - 1, -1, -1):
        for j in range(n + 1):
            # case 1: cut of 'lenghts[i]' is made (ith element is selected)
            profit1 = 0
            if lengths[i] <= j:
                # we can select the item again, so we don't increment the index
                profit1 = prices[i] + dp[i][j - lengths[i]]
            # case 2: cut of 'lenghts[i]' is not made (ith element not selected)
            profit2 = dp[i + 1][j]
            dp[i][j] = max(profit1, profit2)

    return dp[0][n]


# Bottom up dp
# Time: O(m*n) | SPace: O(m*n)
def solve_rod_cutting(lengths, prices, n):
    m = len(prices)

    # init dp
    dp = [[-1 for _ in range(n + 1)] for _ in range(m)]

    # base cases
    # when remaining lenght is 0 (capacity=0), profit is 0
    for i in range(m):
        dp[i][0] = 0

    # since we don't increase index when element is selected, it's value is dependent on another value in the same row
    # better to consider 0 in the tabulation

    # tabulation
    # exclude base cases
    for i in range(m):
        for j in range(1, n + 1):
            # case 1: cut of 'lenghts[i]' is made (ith element is selected)
            profit1, profit2 = 0, 0
            if lengths[i] <= j:
                profit1 = prices[i] + dp[i][j - lengths[i]]
            # case 2: cut of 'lenghts[i]' is not made (ith element not selected)
            if i > 0:
                profit2 = dp[i - 1][j]
            dp[i][j] = max(profit1, profit2)

    return dp[m - 1][n]


# Space optimized
# Time: O(m*n) | Space: O(n)
def solve_rod_cutting(lengths, prices, n):
    m = len(prices)

    # init dp
    dp = [[-1 for _ in range(n + 1)] for _ in range(2)]

    # base cases
    # when remaining lenght is 0 (capacity=0), profit is 0
    for i in range(2):
        dp[i][0] = 0

    # since we don't increase index when element is selected, it's value is dependent on another value in the same row
    # better to consider 0 in the tabulation

    # tabulation
    # exclude base cases
    for i in range(m):
        for j in range(1, n + 1):
            # case 1: cut of 'lenghts[i]' is made (ith element is selected)
            profit1, profit2 = 0, 0
            if lengths[i] <= j:
                profit1 = prices[i] + dp[i % 2][j - lengths[i]]
            # case 2: cut of 'lenghts[i]' is not made (ith element not selected)
            if i > 0:
                profit2 = dp[(i - 1) % 2][j]
            dp[i % 2][j] = max(profit1, profit2)

    return dp[(m - 1) % 2][n]


def main():
    print(solve_rod_cutting([1, 2, 3, 4, 5], [2, 6, 7, 10, 13], 5))


main()
