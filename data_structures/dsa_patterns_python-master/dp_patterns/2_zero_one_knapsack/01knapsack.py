

# Recursive
# Time: O(2^n) | Space: O(n) (stack space for recursion)
def solve_knapsack(profits, weights, capacity):
    def solve_knapsack_helper(i, capacity):
        """Returns max profit using considering the capacity and elements from index i to n-1"""
        # base cases
        # to figure out base cases - look at the inputs of helper that are changing
        if capacity <= 0 or i >= len(weights):
            return 0

        # recursive calls
        # case 1: item at current index 'i' selected
        profit1 = 0
        # we can select the item only if it's weight is <= than capacity
        if weights[i] <= capacity:
            profit1 = profits[i] + solve_knapsack_helper(i + 1, capacity - weights[i])

        # case 1: item at current index 'i' is not selected
        profit2 = solve_knapsack_helper(i + 1, capacity)

        # we want to select the option which gives max profit
        return max(profit1, profit2)

    return solve_knapsack_helper(0, capacity)


# O(n*c) time | O(n*c) space (for the memo)
def solve_knapsack(profits, weights, capacity):
    def solve_knapsack_helper(i, capacity):
        """Returns max profit using considering the capacity and elements from index i to n-1"""
        # base cases
        # to figure out base cases - look at the inputs of helper that are changing
        if capacity <= 0 or i >= len(weights):
            return 0

        # return if already present in dp
        if dp[i][capacity] != -1:
            return dp[i][capacity]

        # recursive calls
        # case 1: item at current index 'i' selected
        profit1 = 0
        # we can select the item only if it's weight is <= than capacity
        if weights[i] <= capacity:
            profit1 = profits[i] + solve_knapsack_helper(i + 1, capacity - weights[i])

        # case 1: item at current index 'i' is not selected
        profit2 = solve_knapsack_helper(i + 1, capacity)

        # add to dp before returning
        dp[i][capacity] = max(profit1, profit2)
        # we want to select the option which gives max profit
        return dp[i][capacity]

    # create memo
    dp = [[-1 for _ in range(capacity + 1)] for _ in range(len(profits))]

    return solve_knapsack_helper(0, capacity)


# Top Down Dp
# O(N*C) time | O(N*C) space -although O time, space is same, O(N) space in stack is saved
def solve_knapsack(profits, weights, capacity):
    # basic checks
    n = len(profits)
    if capacity <= 0 or n == 0 or len(weights) != n:
        return 0

    # initialize dp matrix , can init to 0 but its better to use generic init to -1
    # Need to add a row in this case to init base case from recursive
    dp = [[-1 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # fill base cases
    # capacity 0
    for i in range(n + 1):
        dp[i][0] = 0
    # last row (i>=len(profits))
    for c in range(capacity + 1):
        dp[n][c] = 0

    # Tabulate calculate dp matrix iteratively (using for)
    # Note to calculate dp[i][c] need 2 values from i+1 row, hence go reverse in i
    for i in range(n - 1, -1, -1):
        for c in range(1, capacity + 1):
            # Use eqs from recursive
            p1 = 0
            if weights[i] <= c:
                p1 = profits[i] + dp[i + 1][c - weights[i]]
            p2 = dp[i + 1][c]
            dp[i][c] = max(p1, p2)
    # return top right hand corner - capacity is full, all items >= index 0 considered
    return dp[0][capacity]


# optimized top down dp | Time: O(N*C) | Space:  O(C)
def solve_knapsack(profits, weights, capacity):
    # basic checks
    n = len(profits)
    if capacity <= 0 or n == 0 or len(weights) != n:
        return 0
    # initialize dp matrix , can init to 0 but he said its better to use generic init to -1
    # Need to add a row in this case to init base case from recursive
    dp = [[0 for _ in range(capacity + 1)] for _ in range(2)]

    # Note to calculate dp[i][c] need 2 values from i+1 row, hence go reverse in i
    for i in range(n - 1, -1, -1):
        for c in range(1, capacity + 1):
            # Use eqs from recursive
            p1 = 0
            if weights[i] <= c:
                p1 = profits[i] + dp[(i + 1) % 2][c - weights[i]]
            p2 = dp[(i + 1) % 2][c]
            dp[i % 2][c] = max(p1, p2)
    # return top right hand corner - capcity is full, all items >= index 0 cosnidered
    return dp[0][capacity]


# Bottom up DP
# Time: O(n*c) | Space: O(n*c)
def solve_knapsack(profits, weights, capacity):
    # input validation
    n = len(profits)
    if capacity <= 0 or n == 0 or len(weights) != n:
        return 0

    # init dp
    # dp[i][c] - max profit considering items upto i and capacity c
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n)]

    # base cases
    # capacity = 0
    for i in range(n):
        dp[i][0] = 0

    # for i = 0, you have only the oth item
    # max profit can be if you can take the item, whoch is possible when its weight is less than c
    for c in range(capacity + 1):
        if weights[0] <= c:
            dp[0][c] = profits[0]

    # Tabulation
    for i in range(n):
        for c in range(capacity + 1):
            p1, p2 = 0, 0
            # case 1: item i is selected (if weight <= capacity)
            if weights[i] <= c:
                p1 = profits[i] + dp[i - 1][c - weights[i]]
            # case 2: item i is note selected
            p2 = dp[i - 1][c]

            dp[i][c] = max(p1, p2)

    return dp[n - 1][capacity]


# Otimized Bottom up DP
# Time: O(n*c) | Space: O(c)
def solve_knapsack(profits, weights, capacity):
    # input validation
    n = len(profits)
    if capacity <= 0 or n == 0 or len(weights) != n:
        return 0

    # init dp
    # dp[i][c] - max profit considering items upto i and capacity c
    dp = [[0 for _ in range(capacity + 1)] for _ in range(2)]

    # base cases (capacity =0 already handled in init)
    # for i = 0, you have only the oth item
    # max profit can be if you can take the item, whoch is possible when its weight is less than c
    for c in range(capacity + 1):
        if weights[0] <= c:
            dp[0][c] = profits[0]

    # Tabulation
    for i in range(n):
        for c in range(capacity + 1):
            p1, p2 = 0, 0
            # case 1: item i is selected (if weight <= capacity)
            if weights[i] <= c:
                p1 = profits[i] + dp[(i - 1)%2][c - weights[i]]
            # case 2: item i is note selected
            p2 = dp[(i - 1)%2][c]

            dp[i%2][c] = max(p1, p2)

    return dp[(n - 1)%2][capacity]

# def print_selected_elements(dp, weights, profits, capacity):
#     # print(dp)
#     print(" Selected weights are:", end=" ")
#     i = 0
#     c = capacity
#     while i < len(weights) and c > 0:
#         if dp[i][c] != dp[i + 1][c]:
#             # selected
#             print(weights[i], end=" ")
#             c = c - weights[i]
#         i += 1
#     print()


def main():
    print(solve_knapsack([1, 6, 10, 16], [1, 2, 3, 5], 7))
    print(solve_knapsack([1, 6, 10, 16], [1, 2, 3, 5], 6))
    print(solve_knapsack([4, 5, 3, 7], [2, 3, 1, 4], 5))


main()
