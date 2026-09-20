# There are two cases - element at index i is selected or not selected
# However as we can select an item any number of times, when we select the item i we can consider it for next sleecton
# so we dont increment i, only reduce the capacity
# for TC and SC, view the weights set as n elements + C 1's. Profit for the 1 C's depends on the element choose


# BF
# Time: O(2**(n+c)) | Space: O(n+c)
def solve_knapsack(profits, weights, capacity):
    def solve_knapsack_helper(i, capacity):
        """Returns max profit using considering the capacity and elements from index i to n-1"""
        # base cases
        if capacity <= 0 or i >= n:
            return 0

        # recursive calls
        # case 1: item i selected
        profit1 = 0
        # we can select the item only if its weight is <= the capacity
        if weights[i] <= capacity:
            profit1 = profits[i] + solve_knapsack_helper(i, capacity - weights[i])

        # case 2: item i is not selected
        profit2 = solve_knapsack_helper(i + 1, capacity)

        return max(profit1, profit2)

    n = len(weights)
    return solve_knapsack_helper(0, capacity)


# Memoization
# Time: O((n*c)) | Space: O(n*c)
def solve_knapsack(profits, weights, capacity):
    def solve_knapsack_helper(i, capacity):
        """Returns max profit using considering the capacity and elements from index i to n-1"""
        # base cases
        if capacity <= 0 or i >= n:
            return 0

        # check in memo
        if memo[i][capacity] != -1:
            return memo[i][capacity]

        # recursive calls
        # case 1: item i selected
        profit1 = 0
        # we can select the item only if its weight is <= the capacity
        if weights[i] <= capacity:
            profit1 = profits[i] + solve_knapsack_helper(i, capacity - weights[i])

        # case 2: item i is not selected
        profit2 = solve_knapsack_helper(i + 1, capacity)

        # add to memo
        memo[i][capacity] = max(profit1, profit2)
        return memo[i][capacity]

    n = len(weights)
    memo = [[-1 for _ in range(capacity + 1)] for _ in range(n)]
    return solve_knapsack_helper(0, capacity)


# Top down dp
# Time: (n*c) | Space: O(n*c)
def solve_knapsack(profits, weights, capacity):
    n = len(profits)
    # init dp
    # for top down dp 1 extra row
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # base cases - look at recursion
    for i in range(n + 1):
        dp[i][0] = 0

    for c in range(capacity + 1):
        dp[n][c] = 0

    # tabulation
    # go in reverse order of rows
    for i in range(n - 1, -1, -1):
        for c in range(1, capacity + 1):
            # case 1: item i selected
            profit1 = 0
            # we can select the item only if its weight is <= the capacity
            if weights[i] <= c:
                profit1 = profits[i] + dp[i][c - weights[i]]  # Note - we are using value from same row to fill dp
            # case 2: item i is not selected
            profit2 = dp[i + 1][c]
            dp[i][c] = max(profit1, profit2)

    return dp[0][capacity]


# Bottom up dp
# Time: O(n*c) | Space: O(n*c)
def solve_knapsack(profits, weights, capacity):
    n = len(profits)
    # init dp
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n)]

    # base cases - look at recursion
    # when capacity is 0, profit will be 0
    for i in range(n):
        dp[i][0] = 0

    # In this case for element 0 we could use multiple quantities, hence better to cover in tabulation

    # tabulation
    # exclude base case values
    for i in range(n):  # imp we are filling oth row as part of tabulation and not base case
        for c in range(1, capacity + 1):
            # case 1: item i selected
            profit1 = 0
            # we can select the item only if its weight is <= the capacity
            if weights[i] <= c:
                profit1 = profits[i] + dp[i][c - weights[i]]  # Note - we are using value from same row to fill dp
            # case 2: item i is not selected
            profit2 = dp[i - 1][c]
            dp[i][c] = max(profit1, profit2)

    return dp[n - 1][capacity]


# Space optimized bottom up dp
# Time: O(n*c) | Space: O(c)
def solve_knapsack(profits, weights, capacity):
    n = len(profits)
    # init dp
    dp = [[0 for _ in range(capacity + 1)] for _ in range(2)]

    # base cases - look at recursion
    # when capacity is 0, profit will be 0
    for i in range(2):
        dp[i][0] = 0

    # In this case for element 0 we could use multiple quantities, hence better to cover in tabulation

    # tabulation
    # exclude base case values
    for i in range(n):  # imp we are filling oth row as part of tabulation and not base case
        for c in range(1, capacity + 1):
            # case 1: item i selected
            profit1 = 0
            # we can select the item only if its weight is <= the capacity
            if weights[i] <= c:
                profit1 = profits[i] + dp[i % 2][c - weights[i]]  # Note - we are using value from same row to fill dp
            # case 2: item i is not selected
            profit2 = dp[(i - 1) % 2][c]
            dp[i % 2][c] = max(profit1, profit2)

    return dp[(n - 1) % 2][capacity]



def main():
    print(solve_knapsack([15, 50, 60, 90], [1, 3, 4, 5], 8))
    print(solve_knapsack([15, 50, 60, 90], [1, 3, 4, 5], 6))


main()
