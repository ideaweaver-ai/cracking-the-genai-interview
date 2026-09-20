

# S = sum of array
# the array has to be divided into two subsets of equal sum
# So each subset should have sum S/2
# so if we can create a subset with sum S/2, then the original array can be divided into two subsets of equal sum
# So problem becomes can we find a subset with sum S/2
# Pattern - Knapsack pattern
# We can cover each subset combination recursively - an element can be included in the subset or not
# check if any subset has sum S/2. Return True if we find such a subset

# Time: O(2^n) | Space: O(n)
def can_partition(num):
    def can_partition_helper(i, S):
        """Return True - if any subset has sum S, considering all elements from index n-1 to i"""
        # base cases
        if i == n:
            return S == 0
        # if S == 0:
        #     return True
        #
        # if i >= n:
        #     return False

        # recursive calls
        # case 1: element at index i is included in subset
        # we can only include the element if its value is <= S
        # if the value at element 'i' is greater than S then adding it to subset will make S negative,
        # we should return False in that case
        b1, b2 = False, False
        if num[i] <= S:
            b1 = can_partition_helper(i + 1, S - num[i])
        # case 2: element at index i is not included in subset
        b2 = can_partition_helper(i + 1, S)
        # Return True if we found a subset (True) in either case
        return b1 or b2

    n = len(num)
    sum_ = sum(num)
    if sum_ % 2 != 0 or n == 0:
        # since the array is made of positive integers, the total sum has to be even
        # for the two subsets to have sum S/2
        return False
    return can_partition_helper(0, sum_ / 2)


# Memoized
# Time: O(n*S) | Space: O(n*S)
def can_partition(num):
    def can_partition_helper(i, S):
        """Return True - if any subset has sum S, considering all elements from index n-1 to i"""
        # base cases
        if i == n:
            return S == 0
        # if S == 0:
        #     return True
        #
        # if i >= n:
        #     return False

        # check in memo
        if memo[i][S] != -1:
            return memo[i][S]

        # recursive calls
        # case 1: element at index i is included in subset
        # we can only include the element if its value is <= S
        # if the value at element 'i' is greater than S then adding it to subset will make S negative,
        # we should return False in that case
        b1, b2 = False, False
        if num[i] <= S:
            b1 = can_partition_helper(i + 1, S - num[i])
        # case 2: element at index i is not included in subset
        b2 = can_partition_helper(i + 1, S)
        # Return True if we found a subset (True) in either case
        # Add in memo
        memo[i][S] = b1 or b2
        return memo[i][S]

    # main function
    n = len(num)
    sum_ = sum(num)
    if sum_ % 2 != 0 or n == 0:
        # since the array is made of positive integers, the total sum has to be even
        # for the two subsets to have sum S/2
        return False

    sum_ = int(sum_ / 2)  # ** imp to convert to int as it will be used as array integer
    memo = [[-1 for _ in range(sum_ + 1)] for _ in range(n)]
    return can_partition_helper(0, sum_)


# Dp - Top down
# Time: O(n*S) | Space: O(n*S)
def can_partition(num):
    n = len(num)
    sum_ = sum(num)
    if sum_ % 2 != 0:
        return False
    # S has to be int since we will use it as array index
    S = int(sum_ / 2)

    # define dp - 1 extra row (n) for our base case in top down dp
    dp = [[False for _ in range(S + 1)] for _ in range(n + 1)]

    # base cases
    for i in range(n):
        dp[i][0] = True

    for s in range(S + 1):
        dp[n][s] = False

    # Tabulation
    # imp - rows have to be iterated in reverse order
    for i in range(n - 1, -1, -1):
        for s in range(1, S + 1):
            b1, b2 = False, False
            # case 1: item i is selected
            # we can only include the element if its value is <= S
            if num[i] <= s:
                b1 = dp[i + 1][s - num[i]]
            b2 = dp[i + 1][s]
            dp[i][s] = b1 or b2
    return dp[0][-1]


# dp - bottom up
def can_partition(num):
    n = len(num)
    sum_ = sum(num)
    if sum_ % 2 != 0:
        return False
    # S has to be int since we will use it as array index
    S = int(sum_ / 2)

    # define dp - 1 extra row (n) for our base case in top down dp
    dp = [[False for _ in range(S + 1)] for _ in range(n)]

    # base cases
    for i in range(n):
        # populate the sum = 0 columns, as we can always form '0' sum with an empty set
        dp[i][0] = True

    # with only one number, we can form a subset only when the required sum is
    # equal to its value
    for s in range(S + 1):
        if num[0] <= s:
            dp[0][s] = num[0] == S

    # Tabulation
    for i in range(1, n):
        for s in range(1, S + 1):
            b1, b2 = False, False
            # case 1: item i is selected
            # we can only include the element if its value is <= S
            if num[i] <= s:
                b1 = dp[i - 1][s - num[i]]
            b2 = dp[i - 1][s]
            # case 2: exclude the element
            dp[i][s] = b1 or b2

    # the bottom-right corner will have our answer.
    return dp[n - 1][S]


def main():
    print("Can partition: " + str(can_partition([1, 2, 3, 4])))
    print("Can partition: " + str(can_partition([1, 1, 3, 4, 7])))
    print("Can partition: " + str(can_partition([2, 3, 4, 6])))


main()
