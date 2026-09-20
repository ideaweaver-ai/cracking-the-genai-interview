# Recursion BF
# Time: O(2**n) | Space: O(n) for stack
def count_subsets(num, sum):
    def count_subsets_helper(i, sum):
        """Returns the number of subsets that have sum 'sum' considering elements till index i"""
        # base cases
        if i == n:
            return sum == 0
        # if i == n:
        #     if sum == 0:
        #         return 1
        #     else:
        #         return 0
        # case where sum < 0 is covered in case1 of recursive calls

        # recursive calls
        # case 1: element i included in the subset
        count1, count2 = 0, 0
        # in case num[i] > sum, we cannot get a subset along this path with sum equalling sum
        # because our array consists of only positive nums
        if num[i] <= sum:
            count1 = count_subsets_helper(i + 1, sum - num[i])

        # case 2: element i not included in the subset
        count2 = count_subsets_helper(i + 1, sum)

        return count1 + count2

    n = len(num)
    # Input validation
    if n == 0:
        return 1 if sum == 0 else 0
    return count_subsets_helper(0, sum)


# Memoization
# Time: O(n*s) | Space: O(n*s) for stack
def count_subsets(num, sum):
    def count_subsets_helper(i, sum):
        """Returns the number of subsets that have sum 'sum' considering elements till index i"""
        # base cases
        if i == n:
            return sum == 0
        # case where sum < 0 is covered in case1 of recursive calls

        # check in memo
        if memo[i][sum] != -1:
            return memo[i][sum]

        # recursive calls
        # case 1: element i included in the subset
        count1, count2 = 0, 0
        # in case num[i] > sum, we cannot get a subset along this path with sum equalling sum
        # because our array consists of only positive nums
        if num[i] <= sum:
            count1 = count_subsets_helper(i + 1, sum - num[i])

        # case 2: element i not included in the subset
        count2 = count_subsets_helper(i + 1, sum)

        # add to memo
        memo[i][sum] = count1 + count2

        return memo[i][sum]

    n = len(num)
    # Input validation
    if n == 0:
        return 1 if sum == 0 else 0
    memo = [[-1 for _ in range(sum + 1)] for _ in range(n)]
    return count_subsets_helper(0, sum)


# Top down dp
# Time: O(n*s) time | Space: O(n*s)
def count_subsets(num, sum):
    n = len(num)
    # base case
    # for top down dp - 1 extra row
    dp = [[0 for _ in range(sum + 1)] for _ in range(n + 1)]

    # base cases - look at recursion base cases
    dp[n][0] = 1

    # Tabulation
    # for top down dp iterate over i in reverse order
    # exclude base case values while iteration
    for i in range(n - 1, -1, -1):
        for s in range(sum + 1):
            count1, count2 = 0, 0
            # case 1: element i included in the subset
            if num[i] <= s:
                count1 = dp[i + 1][s - num[i]]
            # case 2: element i not included in the subset
            count2 = dp[i + 1][s]
            dp[i][s] = count1 + count2

    return dp[0][sum]


# Bottom up dp
# Time: O(n*s) | Space: O(n*s)
def count_subsets(num, sum):
    n = len(num)

    dp = [[0 for _ in range(sum + 1)] for _ in range(n)]

    # base cases
    # we can always get sum 0 with an empty set
    for i in range(n):
        dp[i][0] = 1

    # considering only the first element we can get a subset with sum that of the value of 0th element
    if num[0] <= sum:
        dp[0][num[0]] = 1

    # Tabulation
    for i in range(n):
        for s in range(sum + 1):
            count1, count2 = 0, 0
            # case 1: element i included in the subset
            if num[i] <= s:
                count1 = dp[i - 1][s - num[i]]
            # case 2: element i is not included in the subset
            count2 = dp[i - 1][s]
            dp[i][s] = count1 + count2

    return dp[n - 1][sum]


# Space optimized dp
# Time: O(n*s) | Space: O(s)
def count_subsets(num, sum):
    n = len(num)

    dp = [[0 for _ in range(sum + 1)] for _ in range(2)]

    # base cases
    # we can always get sum 0 with an empty set
    for i in range(2):
        dp[i][0] = 1

    # considering only the first element we can get a subset with sum that of the value of 0th element
    if num[0] <= sum:
        dp[0][num[0]] = 1

    # Tabulation
    for i in range(n):
        for s in range(sum + 1):
            count1, count2 = 0, 0
            # case 1: element i included in the subset
            if num[i] <= s:
                count1 = dp[(i - 1) % 2][s - num[i]]
            # case 2: element i is not included in the subset
            count2 = dp[(i - 1) % 2][s]
            dp[i % 2][s] = count1 + count2

    return dp[(n - 1) % 2][sum]







