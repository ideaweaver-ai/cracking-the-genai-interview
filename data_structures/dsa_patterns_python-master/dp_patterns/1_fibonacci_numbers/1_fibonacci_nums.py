# Time: O(2**n) | Space: O(n) for recursion stack
def calculateFibonacci(n):
    "Gives nth fibonacci number"
    # input validation
    if n < 0:
        return -1

    # base cases
    if n <= 1:
        return n

    # recursive calls
    return calculateFibonacci(n - 1) + calculateFibonacci(n - 2)


# Time: O(n) | Space: O(n) for recursion stack
def calculateFibonacci(n):
    def calculateFibonacciHelper(n):
        "Gives nth fibonacci number"
        # input validation
        if n < 0:
            return -1

        # base cases
        if n <= 1:
            return n

        # check in memo
        if memo[n] != -1:
            return memo[n]

        # recursive calls
        # add to memo
        memo[n] = calculateFibonacci(n - 1) + calculateFibonacci(n - 2)
        return memo[n]

    # define memo
    # no need to worry about base case init as they will be taken care of in the helper
    # Note in this case we are following convention of 0 indexing. 0th fin num is 0
    memo = [-1 for _ in range(n + 1)]
    return calculateFibonacciHelper(n)

# Top down dp not possible ? because we have recursion eqs in terms of previous 2 terms (i-1 and i-2)

# Bottom up dp
# O(n) | Space: O(n)
def calculateFibonacci(n):
    # init dp
    dp = [-1 for _ in range(n + 1)]

    # base cases - look at recursion
    dp[0], dp[1] = 0, 1

    # tabulation
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]  # translate from recursion to dp

    return dp[n]


# optimized dp
# Time: O(n) | Space; O(1)
def calculateFibonacci(n):
    # init dp
    # we need only two previous values
    dp = [-1 for _ in range(2)]

    # base cases
    dp[0], dp[1] = 0, 1

    # tabulation
    for i in range(2, n + 1):
        # python calculates RHS first and then assigns to LHS
        # in some other languages we might need dp of size 3
        dp[i % 2] = dp[(i - 1) % 2] + dp[(i - 2) % 2]

    return dp[n % 2]


def main():
    print("5th Fibonacci is ---> " + str(calculateFibonacci(5)))
    print("6th Fibonacci is ---> " + str(calculateFibonacci(6)))
    print("7th Fibonacci is ---> " + str(calculateFibonacci(7)))


main()
