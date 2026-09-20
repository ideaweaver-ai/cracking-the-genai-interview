# Approach1: using a class var to track min
# Time: O(2**(n+t)) | Space: O(n+t)
# class CountChangeHelper:
#     def __init__(self, denominations):
#         self.denominations = denominations
#         self.min_coins = float('inf')
#
#     def count_change_helper(self, i, total, num_coins):
#         # base cases
#         if i == len(self.denominations):
#             if total == 0:
#                 self.min_coins = min(num_coins, self.min_coins)
#             return
#
#         # recursive calls
#         # case 1: coin 1 is selected
#         if self.denominations[i] <= total:
#             self.count_change_helper(i, total - self.denominations[i], num_coins + 1)
#
#         # case 2: coin 1 is not selected
#         self.count_change_helper(i + 1, total, num_coins)
#
#
# def count_change(denominations, total):
#     # main function
#     sol = CountChangeHelper(denominations)
#     sol.count_change_helper(0, total, 0)
#     return sol.min_coins if sol.min_coins != float('inf') else -1


# Time: O(2**(n+t)) | Space: O(n+t)
def count_change(denominations, total):
    def count_change_helper(i, total):
        """Return minimum coins required to achieve remaining total considering deominations from index i to n-1"""
        # base cases
        if i == n:
            if total == 0:
                # when we reach the end, since required total is 0 we can achieve it by 0 coins
                return 0
            else:
                # we should not return 0 in this case, that would mean we can achieve remaining total with 0 coins
                # since we have total remaining after we have reached the end of the array, we need to return inf
                return float('inf')

        # recursive cases
        # case 1: denomination at index i is selected
        count1 = float('inf')
        # we can select the denominaton only if it is <= total
        if denominations[i] <= total:
            # we don't need to change the index as denomination i can be selected again
            count1 = 1 + count_change_helper(i, total - denominations[i])
        # case 2: denomination at index i is not selected
        count2 = count_change_helper(i + 1, total)

        return min(count1, count2)

    n = len(denominations)
    min_coins = count_change_helper(0, total)
    return min_coins if min_coins != float('inf') else -1


# Time: (n*t) | Space: O(n*t)
def count_change(denominations, total):
    def count_change_helper(i, total):
        """Return minimum coins required to achieve remaining total considering deominations from index 0 to i"""
        # base cases
        if i == n:
            if total == 0:
                # when we reach the end, since required total is 0 we can achieve it by 0 coins
                return 0
            else:
                # we should not return 0 in this case, that would mean we can achiever remaining total with 0 coins - best cases
                # since we have total remaining after we have reached the end of the array, we need to return inf
                return float('inf')

        # check memo
        if memo[i][total] != -1:
            return memo[i][total]

        # recursive cases
        # case 1: denomination at index i is selected
        count1 = float('inf')
        # we can select the denominaiton only if it is <= total
        if denominations[i] <= total:
            # we don't need to change the index as denomination i can be selected again
            count1 = 1 + count_change_helper(i, total - denominations[i])
        # case 2: denomination at index i is not selected
        count2 = count_change_helper(i + 1, total)

        memo[i][total] = min(count1, count2)
        return memo[i][total]

    n = len(denominations)
    memo = [[-1 for _ in range(total + 1)] for _ in range(n)]
    min_coins = count_change_helper(0, total)
    return min_coins if min_coins != float('inf') else -1


# Top down dp: O(n*t) | SPace: O(n*t)
def count_change(denominations, total):
    n = len(denominations)
    # dp init
    # top down dp - 1 extra row
    dp = [[-1 for _ in range(total + 1)] for _ in range(n + 1)]

    # base cases - look at recursion
    for t in range(total + 1):
        if t == 0:
            dp[n][t] = 0
        else:
            dp[n][t] = float('inf')

    # tabulation
    # iterate over i in reverse order
    # exclude base cases
    for i in range(n - 1, -1, -1):
        for t in range(total + 1):
            # case 1: denomination at index i is selected
            count1 = float('inf')  # imp - since 0 would mean we already have achieved the total sum with 0 coins
            if denominations[i] <= t:
                count1 = 1 + dp[i][t - denominations[i]]
            # case 2: denomination at index i is not selected
            count2 = dp[i + 1][t]

            dp[i][t] = min(count1, count2)

    return dp[0][total] if dp[0][total] != float('inf') else -1


# Bottom up dp
# Time: O(n*t) | Space: O(n*t)
def count_change(denominations, total):
    n = len(denominations)
    # dp init
    dp = [[-1 for _ in range(total + 1)] for _ in range(n)]

    # base cases - look at recursion
    # when total is 0, we can achieve it with 0 coins
    for i in range(n):
        dp[i][0] = 0

    # since we can consider 0th element multiple times it's better to consider it in tabulation

    # tabulation
    # exclude base cases
    for i in range(n):
        for t in range(1, total + 1):
            # case 1: denomination at index i is selected
            count1, count2 = float('inf'), float(
                'inf')  # imp - since 0 would mean we already have achieved the total sum with 0 coins
            if denominations[i] <= t:
                # we don't change i because we can select the same element multiple itmes
                count1 = 1 + dp[i][t - denominations[i]]
            if i > 0:
                count2 = dp[i - 1][t]
            dp[i][t] = min(count1, count2)

    return dp[n - 1][total] if dp[n - 1][total] != float('inf') else -1


# Space optimized bottom up
# Time: O(n*t) | Space: O(t)
def count_change(denominations, total):
    n = len(denominations)
    # dp init
    dp = [[-1 for _ in range(total + 1)] for _ in range(2)]

    # base cases - look at recursion
    # when total is 0, we can achieve it with 0 coins
    for i in range(2):
        dp[i][0] = 0

    # since we can consider 0th element multiple times it's better to consider it in tabulation

    # tabulation
    # exclude base cases
    for i in range(n):
        for t in range(1, total + 1):
            # case 1: denomination at index i is selected
            count1, count2 = float('inf'), float(
                'inf')  # imp - since 0 would mean we already have achieved the total sum with 0 coins
            if denominations[i] <= t:
                # we don't change i because we can select the same element multiple itmes
                count1 = 1 + dp[i % 2][t - denominations[i]]
            if i > 0:
                count2 = dp[(i - 1) % 2][t]
            dp[i % 2][t] = min(count1, count2)

    return dp[(n - 1) % 2][total] if dp[(n - 1) % 2][total] != float('inf') else -1


def main():
    print(count_change([1, 2, 3], 5))
    print(count_change([1, 2, 3], 11))
    print(count_change([1, 2, 3], 7))
    print(count_change([3, 5], 7))


main()
