# Time: O(2**(n+t)) | Space: O(n)
def count_ribbon_pieces(ribbonLengths, total):
    def count_ribbon_pieces_helper(i, total):
        """Returns the max number of pieces that can be made considering elements from i to n and the remaining total"""
        # base case
        # we need to form the exact total length with the cut lengths
        # we can solve similar problem, where total length may not be exactly equal to sum of cut lengths
        if i == n:
            return 0 if total == 0 else -float('inf')
        # recursive calls
        # case 1: ribbonLengths[i] is cut (element i is included in subset)
        count1 = -float('inf')  # since we need max num of pieces we can initialize to -1
        # we can make the cur of lenght ribbonLength[i] if it is <= total
        if ribbonLengths[i] <= total:
            # since we can make the cut of length ribbonLenght[i] again, we don't increment the index i
            count1 = 1 + count_ribbon_pieces_helper(i, total - ribbonLengths[i])
        # case 2: ribbonLengths[i] cut is not made(element i is not included in the subset)
        count2 = count_ribbon_pieces_helper(i + 1, total)
        return max(count1, count2)

    n = len(ribbonLengths)
    max_pieces = count_ribbon_pieces_helper(0, total)
    return max_pieces if max_pieces != -float('inf') else -1


# Time: O(n*t) | Space: O(n*t)
def count_ribbon_pieces(ribbonLengths, total):
    def count_ribbon_pieces_helper(i, total):
        """Returns the max number of pieces that can be made considering elements from i to n and the remaining total"""
        # base case
        # we need to form the exact total length with the cut lengths
        # we can solve similar problem, where total length may not be exactly equal to sum of cut lengths
        if i == n:
            return 0 if total == 0 else -float('inf')

        # check in memo
        if memo[i][total] != -1:
            return memo[i][total]

        # recursive calls
        # case 1: ribbonLengths[i] is cut (element i is included in subset)
        count1 = -float('inf')  # since we need max num of pieces we need to initialize -float('inf')
        # we can make the cut of length ribbonLength[i] if it is <= total
        if ribbonLengths[i] <= total:
            # since we can make the cut of length ribbonLenght[i] again, we don't increment the index i
            count1 = 1 + count_ribbon_pieces_helper(i, total - ribbonLengths[i])
        # case 2: ribbonLengths[i] cut is not made(element i is not included in the subset)
        count2 = count_ribbon_pieces_helper(i + 1, total)

        # Add to memo
        memo[i][total] = max(count1, count2)
        return memo[i][total]

    n = len(ribbonLengths)
    memo = [[-1 for _ in range(total + 1)] for _ in range(n)]
    max_pieces = count_ribbon_pieces_helper(0, total)
    return max_pieces if max_pieces != -float('inf') else -1


# Top down dp
# Time: O(n*t) | Space: O(n*t)
def count_ribbon_pieces(ribbonLengths, total):
    n = len(ribbonLengths)
    # init dp
    # top down dp requires one more row
    dp = [[-float('inf') for _ in range(total + 1)] for _ in range(n + 1)]  # can also init to -float('inf')

    # base cases - look at recursion
    for t in range(total + 1):
        if t == 0:
            dp[n][t] = 0
        else:
            dp[n][t] = -float('inf')

    # tabulation
    # iterate over i in reverse order
    # exclude base cases
    for i in range(n - 1, -1, -1):
        for t in range(total + 1):
            # case 1: ribbonLengths[i] is cut (element i is included in subset)
            count1 = -float('inf')  # since we need max num of pieces we need to initialize -float('inf')
            # we can make the cut of length ribbonLength[i] if it is <= total
            if ribbonLengths[i] <= t:
                # since we can make the cut of length ribbonLenght[i] again, we don't increment the index i
                count1 = 1 + dp[i][t - ribbonLengths[i]]
            # case 2: ribbonLengths[i] cut is not made(element i is not included in the subset)
            count2 = dp[i + 1][t]
            dp[i][t] = max(count1, count2)
    return dp[0][total] if dp[0][total] != -float('inf') else -1


# Bottom up dp
# Time: O(2**(n+t)) | Space: O(n)
def count_ribbon_pieces(ribbonLengths, total):
    n = len(ribbonLengths)
    # init dp
    dp = [[-float('inf') for _ in range(total + 1)] for _ in range(n)]  # can also init to -float('inf')

    # base cases
    # When total is 0, i can achieve it max 0 cut pieces
    for i in range(n):
        dp[i][0] = 0
    # since we can cut ribbonLengths[0] multiple times, it's better to consider it in tabulation

    # tabulation
    # exclude base cases
    for i in range(n):
        for t in range(1, total + 1):
            # case 1: ribbonLengths[i] is cut (element i is included in subset)
            count1 = -float('inf')  # since we need max num of pieces we need to initialize -float('inf')
            # we can make the cut of length ribbonLength[i] if it is <= total
            if ribbonLengths[i] <= t:
                # since we can make the cut of length ribbonLenght[i] again, we don't increment the index i
                count1 = 1 + dp[i][t - ribbonLengths[i]]
            # case 2: ribbonLengths[i] cut is not made(element i is not included in the subset)
            count2 = dp[i - 1][t]

            dp[i][t] = max(count1, count2)
    return dp[n - 1][total] if dp[n - 1][total] != -float('inf') else -1


# Optimized bottom up dp
# Time: O(n*t) | Space: O(t)
def count_ribbon_pieces(ribbonLengths, total):
    n = len(ribbonLengths)
    # init dp
    dp = [[-float('inf') for _ in range(total + 1)] for _ in range(2)]  # can also init to -float('inf')

    # base cases
    # When total is 0, i can achieve it max 0 cut pieces
    for i in range(2):
        dp[i][0] = 0
    # since we can cut ribbonLengths[0] multiple times, it's better to consider it in tabulation

    # tabulation
    # exclude base cases
    for i in range(n):
        for t in range(1, total + 1):
            # case 1: ribbonLengths[i] is cut (element i is included in subset)
            count1 = -float('inf')  # since we need max num of pieces we need to initialize -float('inf')
            # we can make the cut of length ribbonLength[i] if it is <= total
            if ribbonLengths[i] <= t:
                # since we can make the cut of length ribbonLenght[i] again, we don't increment the index i
                count1 = 1 + dp[i % 2][t - ribbonLengths[i]]
            # case 2: ribbonLengths[i] cut is not made(element i is not included in the subset)
            count2 = dp[(i - 1) % 2][t]

            dp[i % 2][t] = max(count1, count2)
    return dp[(n - 1) % 2][total] if dp[(n - 1) % 2][total] != -float('inf') else -1


def main():
    print(count_ribbon_pieces([2, 3, 5], 5))
    print(count_ribbon_pieces([2, 3], 7))
    print(count_ribbon_pieces([3, 5, 7], 13))
    print(count_ribbon_pieces([3, 5], 7))


main()
