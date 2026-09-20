def can_partition(num):
    def can_partition_helper(i, s1, s2):
        """Returns min difference between sum of subset1 and subset2 considering all elements from 0 to i"""
        # base case
        if i == n:
            return abs(s1 - s2)
        # recursive calls
        # case 1: element at 'i' included in subset1
        diff1 = can_partition_helper(i + 1, s1 + num[i], s2)
        # case 2: element at 'i' is not included in subset2
        diff2 = can_partition_helper(i + 1, s1, s2 + num[i])

        # return min of the two differences
        return min(diff1, diff2)

    n = len(num)
    return can_partition_helper(0, 0, 0)


# Time: O(n*S) | Space: O(n)
def can_partition(num):
    def can_partition_helper(i, s1, s2):
        """Returns min difference between sum of subset1 and subset2 considering all elements from 0 to i"""
        # base case
        if i == n:
            return abs(s1 - s2)

        if memo[i][s1] != -1:
            return memo[i][s1]
        # recursive calls
        # case 1: element at 'i' included in subset1
        diff1 = can_partition_helper(i + 1, s1 + num[i], s2)
        # case 2: element at 'i' is not included in subset2
        diff2 = can_partition_helper(i + 1, s1, s2 + num[i])

        # Add to memo
        # return min of the two differences
        memo[i][s1] = min(diff1, diff2)

        return memo[i][s1]

    n = len(num)
    s = sum(num)
    memo = [[-1 for _ in range(s + 1)] for _ in range(n)]
    return can_partition_helper(0, 0, 0)


# Top down dp
# Time: O(n*s) | Space: O(n*s)
def can_partition(num):
    # init dp
    n = len(num)
    s = sum(num)
    # for dp the two variables are element index 'i' and sum of subset s1
    # imp top down dp should have an extra row for i
    dp = [[-1 for _ in range(s + 1)] for _ in range(n + 1)]

    # base case, when i = n the min difference will be abs(s2-s1)
    # our column axis var is s1, so s2 = s-s1. hence min diff = abs(s2-s1) = abs(s-2s1)
    for s1 in range(s + 1):
        s2 = s - s1
        dp[n][s1] = abs(s1 - s2)

    # Tabulation
    # for top down tabulation we iterate i in reverse
    # exclude base case values during iteration
    for i in range(n - 1, -1, -1):
        # Tricky, in dp table we consider all the possible values of s1
        # we need to be careful that we calculate only those values which are possible
        # eg. in recursion s1 can reach a max value of s including all nums
        # but when we are iterating in a row in dp, s1's possible values are 0 to s
        # so if we consider s+num[i] clearly that value is not possible for s1
        # and consequenlty the complimentary value for s2 is also not possible

        s1 = 0
        while s1 + num[i] <= s:
            diff1 = dp[i + 1][s1 + num[i]]
            # since s1 and s2 are complementary, if s1 is not possible, corresponding s2 is also not possible
            # hence both these calculations should be under while loop
            diff2 = dp[i + 1][s1]
            dp[i][s1] = min(diff1, diff2)
            s1 += 1
    # print(dp)
    return dp[0][0]


# Bottom up dp -keeping same problem definition
# Time: O(n*s) | Space: O(n*s)
def can_partition(num):
    S = sum(num)
    n = len(num)

    # memo
    dp = [[float('inf') for _ in range(S + 1)] for _ in range(n)]

    # initialize dp
    # base cases - consider only 0th element

    dp[0][num[0]] = abs(S - num[0] - num[0])
    dp[0][0] = num[0]  # since num[0] part of s2

    # Tabulation
    # imp - perform tabulation by excluding the base cases
    s = num[0]  # total sum considering i elements
    for i in range(1, n):
        s += num[i]
        for s1 in range(1, S + 1):
            diff1, diff2 = float('inf'), float('inf')
            # Case 1 : include element i in subset s1
            # check if it is possible to create sum s1 including current element i
            # this is possible when s1-num[i] gives a positive index, dp[i-1][s1-num[i]] is possible i.e not inifinity
            # in that case the diff is then s2 = S- s1, diff = abs(s2-s1) = abs(S-2*s1
            if s1 - num[i] >= 0 and dp[i - 1][s1 - num[i]] != float('inf'):
                diff1 = abs(S - 2 * s1)
            # case 2: item i not selected
            diff2 = dp[i - 1][s1]   # no need to check, in case it is not possible d2 will automatically be float('inf
            dp[i][s1] = min(diff1, diff2)

    return min(dp[n - 1])

# # Bottom up dp
# # Time: O(n*s) | Space: O(n*s)
# # The best difference we can obtain is 0, when subset1 and subset2 both have sum S/2
# # so the question changes to can we find a subset with sum s/2
# # if not find the closest sum to it
# def can_partition(num):
#     n = len(num)
#     s = sum(num)
#     dp = [[False for _ in range(int(s / 2) + 1)] for _ in range(n)]
#
#     # base cases
#     # we can get sum of subset 0 with an empty set, hence this is always possible (considering [0], [0,1], [0,1,2] ..)
#     for i in range(n):
#         dp[i][0] = True
#     # considering only item at index 0, the subset sum is possible if it can be selected
#     for s1 in range(int(s / 2) + 1):
#         dp[0][s1] = num[0] == s1
#
#     # tabulation
#     # imp - perform tabulation by excluding the base cases
#     for i in range(1, n):
#         for s1 in range(1, int(s / 2) + 1):
#             b1, b2 = False, False
#             if s1 >= num[i]:
#                 b1 = dp[i - 1][s1 - num[i]]
#             b2 = dp[i - 1][s1]
#             dp[i][s1] = b1 or b2
#
#     # print(dp)
#
#     # find the value of s1 closest to s/2
#     for s1 in range(int(s / 2), -1, -1):
#         if dp[n - 1][s1]:
#             # we found the value of s1 closest to s/2
#             break
#
#     s2 = s - s1
#     return abs(s2 - s1)
#
#
# # Optimized bottom up dp
# # Time: O(n*s) | Space: (s)
# def can_partition(num):
#     n = len(num)
#     s = sum(num)
#     dp = [[False for _ in range(int(s / 2) + 1)] for _ in range(2)]
#
#     # base cases
#     # we can get sum of subset 0 with an empty set, hence this is always possible (considering [0], [0,1], [0,1,2] ...etc.)
#     for i in range(2):
#         dp[i][0] = True
#     # considering ly item at index 0, the subset sum is possible if it can be selected
#     for s1 in range(int(s / 2) + 1):
#         dp[0][s1] = num[0] == s1
#
#     # tabulation
#     # imp - perform tabulation by excluding the base cases
#     for i in range(1, n):
#         for s1 in range(1, int(s / 2) + 1):
#             b1, b2 = False, False
#             if s1 >= num[i]:
#                 b1 = dp[(i - 1) % 2][s1 - num[i]]
#             b2 = dp[(i - 1) % 2][s1]
#             dp[i % 2][s1] = b1 or b2
#
#     # print(dp)
#
#     # find the value of s1 closest to s/2
#     for s1 in range(int(s / 2), -1, -1):
#         if dp[(n - 1) % 2][s1]:
#             # we found the value of s1 closest to s/2
#             break
#
#     s2 = s - s1
#     return abs(s2 - s1)


def main():
    print("Can partition: " + str(can_partition([1, 2, 3, 9])))
    print("Can partition: " + str(can_partition([1, 2, 7, 1, 5])))
    print("Can partition: " + str(can_partition([1, 3, 100, 4])))


main()
