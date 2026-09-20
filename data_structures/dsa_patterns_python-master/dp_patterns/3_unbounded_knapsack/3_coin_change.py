# O(2**(n+t)) | Space: O(n+t)
def count_change(denominations, total):
    def count_change_helper(i, total):
        """Returns number of ways the remaining total can be created with denominations from 0 to i considered"""
        # base cases
        if i == n:
            return 1 if total == 0 else 0

        # recursion calls
        # case1: coin i is included in the total(subset)
        # we can inlcude teh coin only if its denomination(value) is <= total
        count1 = 0
        if denominations[i] <= total:
            # we don't need to increment the index in recursion call as same denomination can be selected again
            count1 = count_change_helper(i, total - denominations[i])

        # case2: coin i is not included in the total(subset)
        count2 = count_change_helper(i + 1, total)

        return count1 + count2

    n = len(denominations)
    return count_change_helper(0, total)


# Time: O(n*t) | Space: O(n*t)
def count_change(denominations, total):
    def count_change_helper(i, total):
        """Returns number of ways the remaining total can be created with denominations from 0 to i considered"""
        # base cases
        if i == n:
            return 1 if total == 0 else 0

        # check in memo
        if memo[i][total] != -1:
            return memo[i][total]

        # recursion calls
        # case1: coin i is included in the total(subset)
        # we can inlcude teh coin only if its denomination(value) is <= total
        count1 = 0
        if denominations[i] <= total:
            # we don't need to increment the index in recursion call as same denomination can be selected again
            count1 = count_change_helper(i, total - denominations[i])

        # case2: coin i is not included in the total(subset)
        count2 = count_change_helper(i + 1, total)

        # Add to memo
        memo[i][total] = count1 + count2
        return memo[i][total]

    n = len(denominations)
    memo = [[-1 for _ in range(total + 1)] for _ in range(n)]
    return count_change_helper(0, total)


# Time: O(n*t) | Space: O(n*t)
def count_change(denominations, total):
    n = len(denominations)
    # dp init
    # for top down dp one extra row
    dp = [[-1 for _ in range(total + 1)] for _ in range(n + 1)]

    # base cases - look at recursion
    for t in range(total + 1):
        if t == 0:
            dp[n][t] = 1
        else:
            dp[n][t] = 0

    # tabulation
    # iterate in reverse order over i
    # exclude base cases
    for i in range(n - 1, -1, -1):
        for t in range(total + 1):  # we haven't handled t = 0 in base case
            # case1: coin i is included in the total(subset)
            # we can inlcude teh coin only if its denomination(value) is <= total
            count1 = 0
            if denominations[i] <= t:
                count1 = dp[i][t - denominations[i]]
            # case2: coin i is not included in the total(subset)
            count2 = dp[i + 1][t]
            dp[i][t] = count1 + count2

    return dp[0][total]


# Bottom up dp
# Time: O(n*t) | Space: O(n*t)
def count_change(denominations, total):
    n = len(denominations)
    # dp init
    dp = [[-1 for _ in range(total + 1)] for _ in range(n)]

    # base cases - look at recursion
    # i can have a total without selecting any denomination (empty set)
    # so we can fill the colum for t=0 with 0
    for i in range(n):
        dp[i][0] = 1
    # since we can consider element 0 multiple times it is easier to handle it in tabulation

    # tabulation
    for i in range(n):
        for t in range(1, total + 1):
            # case1: coin i is included in the total(subset)
            # we can inlcude teh coin only if its denomination(value) is <= total
            count1, count2 = 0, 0
            if denominations[i] <= t:
                count1 = dp[i][t - denominations[i]]
            if i > 0:
                count2 = dp[i - 1][t]
            dp[i][t] = count1 + count2

    return dp[n - 1][total]


# Optimized dp
# Time: O(n*t) | Space: O(t)
def count_change(denominations, total):
    n = len(denominations)
    # dp init
    dp = [[-1 for _ in range(total + 1)] for _ in range(2)]

    # base cases - look at recursion
    # i can have a total without selecting any denomination (empty set)
    # so we can fill the colum for t=0 with 0
    for i in range(2):
        dp[i][0] = 1
    # since we can consider element 0 multiple times it is easier to handle it in tabulation

    # tabulation
    for i in range(n):
        for t in range(1, total + 1):
            # case1: coin i is included in the total(subset)
            # we can include the coin only if its denomination(value) is <= total
            count1, count2 = 0, 0
            if denominations[i] <= t:
                count1 = dp[i % 2][t - denominations[i]]
            # imp to check i > 0
            if i > 0:
                count2 = dp[(i - 1) % 2][t]
            dp[i % 2][t] = count1 + count2

    return dp[(n - 1) % 2][total]


def main():
    print(count_change([1, 2, 3], 5))


main()
