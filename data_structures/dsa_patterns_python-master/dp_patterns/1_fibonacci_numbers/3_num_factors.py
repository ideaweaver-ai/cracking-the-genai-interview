# Time: O(3**n) | Space: O(n)
def count_ways(n):
    """Returns num of ways n (remaining) can be expressed as sum of 1,3 or 4"""
    # base cases
    if n == 0:
        # if i am left 0 steps, we can do it in 1 way - take no steps
        return 1
    elif n == 1:
        return 1
    # remaining cases even taking 3 nd 4 steps can be broken down into these base cases following the recursive calls

    # recursive calls
    num_ways_one, num_ways_three, num_ways_four = 0, 0, 0
    # since we took one step we are left with n-1 steps
    if n >= 1:  # we don't need to check this as it is covered in base cases
        num_ways_one = count_ways(n - 1)

    if n >= 3:
        # since we took one step we are left with n-1 steps
        num_ways_three = count_ways(n - 3)

    if n >= 4:
        # since we took one step we are left with n-4 steps
        num_ways_four = count_ways(n - 4)

    return num_ways_one + num_ways_three + num_ways_four


# Memoization
# Time: O(n) | Space: O(n)
def count_ways(n):
    # for memoization we need a separate helper function because memo needs to be defined outside the helper
    def count_ways_helper(n):
        """Returns num of ways n (remaining) can be expressed as sum of 1,3 or 4"""
        # base cases
        if n == 0:
            # if i am left 0 steps, we can do it in 1 way - take no steps
            return 1
        elif n == 1:
            return 1
        # remaining cases even taking 3 nd 4 steps can be broken down into these base cases following recursive calls

        # check in memo
        if memo[n] != -1:
            return memo[n]

        # recursive calls
        num_ways_one, num_ways_three, num_ways_four = 0, 0, 0
        # since we took one step we are left with n-1 steps
        if n >= 1:  # we don't need to check this as it is covered in base cases
            num_ways_one = count_ways_helper(n - 1)

        if n >= 3:
            # since we took one step we are left with n-1 steps
            num_ways_three = count_ways_helper(n - 3)

        if n >= 4:
            # since we took one step we are left with n-4 steps
            num_ways_four = count_ways_helper(n - 4)

        # Add to memo
        memo[n] = num_ways_one + num_ways_three + num_ways_four
        return memo[n]

    memo = [-1 for _ in range(n + 1)]
    return count_ways_helper(n)


# Bottom up dp
# Time: O(n) | Space: O(n)
def count_ways(n):
    # init dp
    dp = [-1 for _ in range(n + 1)]

    # base cases - see recursion
    dp[0], dp[1] = 1, 1

    # tabulation
    # exclude base cases
    for i in range(2, n + 1):
        num_ways_one, num_ways_three, num_ways_four = 0, 0, 0
        # since we took one step we are left with n-1 steps
        if i >= 1:  # we don't need to check this as it is covered in base cases
            num_ways_one = dp[i - 1]

        if i >= 3:
            # since we took one step we are left with n-1 steps
            num_ways_three = dp[i - 3]

        if i >= 4:
            # since we took one step we are left with n-4 steps
            num_ways_four = dp[i - 4]

        dp[i] = num_ways_one + num_ways_three + num_ways_four

    return dp[n]


# Optimized dp
# Time: O(n) | Space: O(1)
def count_ways(n):
    # init dp
    # ** vimp -  although we have 3 values dependent values, we need 4 values as go upto the 4th previous values.
    # we need that to have modulo at correct index
    # e.g if n = 5, (5-1)%3 = 1, (5-4)%3 = 1 -> so these two nos will override
    dp = [-1 for _ in range(4)]

    # base cases - see recursion
    dp[0], dp[1] = 1, 1

    # tabulation
    # exclude base cases
    for i in range(2, n + 1):
        num_ways_one, num_ways_three, num_ways_four = 0, 0, 0
        # since we took one step we are left with n-1 steps
        if i >= 1:  # we don't need to check this as it is covered in base cases
            num_ways_one = dp[(i - 1) % 4]

        if i >= 3:
            # since we took one step we are left with n-1 steps
            num_ways_three = dp[(i - 3) % 4]

        if i >= 4:
            # since we took one step we are left with n-4 steps
            num_ways_four = dp[(i - 4) % 4]

        dp[i % 4] = num_ways_one + num_ways_three + num_ways_four

    return dp[n % 4]


def main():
    print(count_ways(4))
    print(count_ways(5))
    print(count_ways(6))


main()
