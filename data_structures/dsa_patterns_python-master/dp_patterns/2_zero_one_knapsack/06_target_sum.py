# Note using currentSum == S can simplify recursion but makes dp very difficult


# Time: O(2**n) | Space: O(n) for stack
def find_target_subsets(num, s):
    def find_target_subsets_helper(i, s):
        """Returns the number of subsets that give sum s considering elements till index i"""
        # base cases
        if i == n:
            return 1 if s == 0 else 0

        # recursion calls
        # case 1: add +num[i] to the subset, thereby reducing required sum. s = s-num[i]
        # also note in this case required sum s can go negative and still become 0 later
        count1 = find_target_subsets_helper(i + 1, s - num[i])
        # case2: add -num[i] to the subset, thereby increasing required sum. s = s+num[i]
        count2 = find_target_subsets_helper(i + 1, s + num[i])

        return count1 + count2

    n = len(num)
    if n == 0:
        return 1 if s == 0 else 0
    return find_target_subsets_helper(0, s)


# Memoization - *** vimp
# Time: O(n*s) | Space: O(n*s)
def find_target_subsets(num, s):
    def find_target_subsets_helper(i, target_sum_rec):
        """Returns the number of subsets that give sum s considering elements till index i"""
        # base cases
        if i == n:
            return 1 if target_sum_rec == 0 else 0

        # check in memo
        # key has to be immutable - hence tuple
        if (i, target_sum_rec) in memo:
            return memo[(i, target_sum_rec)]

        # recursion calls
        count1, count2 = 0, 0
        # case 1: add +num[i] to the subset, thereby reducing required sum. s = s-num[i]
        # also note in this case required sum s can go negative and still become 0 later
        count1 = find_target_subsets_helper(i + 1, target_sum_rec - num[i])
        # case2: add -num[i] to the subset, thereby increasing required sum. s = s+num[i]
        count2 = find_target_subsets_helper(i + 1, target_sum_rec + num[i])

        # Add to memo
        memo[(i, target_sum_rec)] = count1 + count2

        return memo[(i, target_sum_rec)]

    n = len(num)
    if n == 0:
        return 1 if s == 0 else 0
    # Tricky
    # since we can add negative of any num to the subset, the max range that s can go is s+sum(num)
    # also our s can become negative in recursion calls, for e.g. adding all nums to subsets can make s negative
    # and we cannot break out of our call if required sum 's' becomes -ive, as it may become 0 later
    # hence use dict for memo
    sum_ = sum(num)
    memo = {}
    return find_target_subsets_helper(0, s)


# Tabulation O(n*totalSum) time | O(n*totalSum) space
def find_target_subsets(num, S):
    n = len(num)
    totalSum = sum(num)
    if n == 0 or S > totalSum or S < -totalSum:
        return 0
    dp = [[0 for _ in range(2*totalSum+1)] for _ in range(n+1)] # y index is S (target sum) - sum of subest values. Hence shift
    shift = totalSum - S  # shift required to make y index +ive

    # dp base case
    dp[n][shift] = 1

    for i in range(n-1, -1, -1):
        for s in range(2*totalSum+1):
            count1, count2 = 0, 0
            if s+num[i] <= 2*totalSum:
                count1 = dp[i+1][s+num[i]]
            if s-num[i] >= 0:
                count2 = dp[i+1][s-num[i]]
            dp[i][s] = count1 + count2
    # print(dp)
    return max(dp[0])  # The way we have framed the problem is shift +S (current value) +- nums[i] can be any value in top row and any of them can reach the bottom row cell having val 1



def main():
    print("Total ways: " + str(find_target_subsets([1, 1, 2, 3], 1)))
    print("Total ways: " + str(find_target_subsets([1, 2, 7, 1], 9)))


main()
