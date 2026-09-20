# Recursive O(2^n) time | O(n) space
def can_partition(nums, S):
    if S < 0 or len(nums) == 0:
        return False
    return helper(nums, S, 0)


def helper(nums, S, i):
    n = len(nums)
    # base case
    if i == n:
        return S == 0
    # Recursive
    can1, can2 = False, False
    if nums[i] <= S:
        can1 = helper(nums, S - nums[i], i + 1)
    can2 = helper(nums, S, i + 1)
    return can1 or can2


# Memoized O(n*S) time | O(n*S) space
def can_partition(nums, S):
    dp = [[None for _ in range(S+1)] for _ in range(len(nums))]
    if S < 0 or len(nums) == 0:
        return False
    return helper(nums, S, 0, dp)


def helper(nums, S, i, dp):
    n = len(nums)
    # base case
    if i == n:
        return S == 0
    # check memo
    if dp[i][S] is not None:
        return dp[i][S]

    # Recursive
    can1, can2 = False, False
    if nums[i] <= S:
        can1 = helper(nums, S - nums[i], i + 1)
    can2 = helper(nums, S, i + 1)
    dp[i][S] = can1 or can2
    return dp[i][S]

# Tabulation O(n*S) time | O(n*S) space
def can_partition(nums, S):
    # check inputs
    if len(nums) == 0 or S < 0:
        return False
    n = len(nums)
    dp = [[False for _ in range(S+1)] for _ in range(n+1)]
    for i in range(n):
        dp[i][0] = True
    for s in range(1, S+1):
        dp[n][s] = False  # Not required in this case - general
    for i in range(n-1, -1, -1):
        for s in range(1, S+1):
            can1, can2 = False, False
            if nums[i] <= s: #imp - s var and total sum S
                can1 = dp[i+1][s-nums[i]]
            can2 = dp[i+1][s]
            dp[i][s] = can1 or can2
    return dp[0][S]


# Tabulation optimized O(n*S) time | O(S) space
def can_partition(nums, S):
    # check inputs
    if len(nums) == 0 or S < 0:
        return False
    n = len(nums)
    dp = [[False for _ in range(S+1)] for _ in range(2)]
    for i in range(n):
        dp[i % 2][0] = True
    for s in range(S+1):
        dp[n % 2][s] = False  # Not required in this case - general
    for i in range(n-1, -1, -1):
        for s in range(1, S+1):
            can1, can2 = False, False
            if nums[i] <= s:  # imp - s var and total sum S
                can1 = dp[(i+1) % 2][s-nums[i]]
            can2 = dp[(i+1) % 2][s]
            dp[i % 2][s] = can1 or can2
    return dp[0][S]


def main():
    print("Can partition: " + str(can_partition([1, 2, 3, 7], 6)))
    print("Can partition: " + str(can_partition([1, 2, 7, 1, 5], 10)))
    print("Can partition: " + str(can_partition([1, 3, 4, 8], 6)))


main()
