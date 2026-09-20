# Time: O(3**n) | Space: O(n)
def count_ways(n):
    """Returns the number of ways, taking 1,2,3 step options and considering the remaining steps n"""
    # since additional inputs are not required, we don't need a helper function

    # base cases
    # if 0 steps are remaining, that can be achieved in 1 way - taking no steps
    if n == 0:
        return 1

    # 2 and 3 steps can be reduced to base cases of 0 and 1 case

    # recursion calls
    ways_one_step, ways_two_step, ways_three_step = 0, 0, 0

    # since we take 1 step, remaining steps is n-1
    if n >= 1:
        ways_one_step = count_ways(n - 1)

    if n >= 2:
        # we can two steps only if n >= 2
        # since we take 2 steps, remaining steps is n-2
        ways_two_step = count_ways(n - 2)

    if n >= 3:
        # we can three steps only if n >= 3
        # since we take 3 steps, remaining steps is n-3
        ways_three_step = count_ways(n - 3)

    return ways_one_step + ways_two_step + ways_three_step


# Time: O(n) | Space: O(n)
def count_ways(n):
    def count_ways_helper(i):
        """Returns the number of ways, taking 1,2,3 step options and considering the remaining steps i"""
        # since additional inputs are not required, we don't need a helper function

        # base cases
        # if 0 steps are remaining, that can be achieved in 1 way
        # all other cases will be an addition of this base case and some invalid values
        if n == 0:
            return 1

        # check in memo
        if memo[i] != -1:
            return memo[i]

        # recursion calls
        ways_one_step, ways_two_step, ways_three_step = 0, 0, 0

        # since we take 1 step, remaining steps is n-1
        if n >= 1:
            ways_one_step = count_ways(n - 1)

        if n >= 2:
            # we can two steps only if n >= 2
            # since we take 2 steps, remaining steps is n-2
            ways_two_step = count_ways(n - 2)

        if n >= 3:
            # we can three steps only if n >= 3
            # since we take 3 steps, remaining steps is n-3
            ways_three_step = count_ways(n - 3)

        memo[i] = ways_one_step + ways_two_step + ways_three_step
        return memo[i]

    memo = [-1 for _ in range(n + 1)]
    return count_ways_helper(n)


# Dp - Tabulation
# Time: O(n) | Space: O(n)
def count_ways(n):
    # init dp
    dp = [0 for _ in range(n + 1)]

    # base cases -  see recursion
    dp[0] = 1

    # tabulation
    # exclude base cases
    for i in range(1, n + 1):

        ways_one_step, ways_two_step, ways_three_step = 0, 0, 0
        # we can one step only if i >= 1, but since we are starting from 1 ideally we don't need to check this condition
        # since we take 1 step, remaining steps is i-1
        if i >= 1:
            ways_one_step = dp[i - 1]

        # since we take 2 steps, remaining steps is i-2
        if i >= 2:
            ways_two_step = dp[i - 2]

        # since we take 3 steps, remaining steps is i-3
        if i >= 3:
            # we can three steps only if i >= 3
            ways_three_step = dp[i - 3]

        dp[i] = ways_one_step + ways_two_step + ways_three_step

    return dp[n]


# Optimized dp
# Time: (n) | Space: O(1)
def count_ways(n):
    # init dp
    dp = [0 for _ in range(3)]

    # base cases -  see recursion
    dp[0] = 1

    # tabulation
    # exclude base cases
    for i in range(1, n + 1):

        ways_one_step, ways_two_step, ways_three_step = 0, 0, 0
        # we can one step only if i >= 1, but since we are starting from 1 ideally we don't need to check this condition
        # since we take 1 step, remaining steps is i-1
        if i >= 1:
            ways_one_step = dp[(i - 1)%3]

        # since we take 2 steps, remaining steps is i-2
        if i >= 2:
            ways_two_step = dp[(i - 2)%3]

        # since we take 3 steps, remaining steps is i-3
        if i >= 3:
            # we can three steps only if i >= 3
            ways_three_step = dp[(i - 3)%3]

        dp[i%3] = ways_one_step + ways_two_step + ways_three_step

    return dp[n%3]


def main():
    print(count_ways(3))
    print(count_ways(4))
    print(count_ways(5))


main()

