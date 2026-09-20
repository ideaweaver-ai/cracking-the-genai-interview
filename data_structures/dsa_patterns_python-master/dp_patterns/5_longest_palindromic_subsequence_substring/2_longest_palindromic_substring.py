# Top down DP
# Time: O(n**2) | Space: O(n**2)
def find_LPS_length(st):
    if not st:
        return False

    # init vars
    n = len(st)
    max_len = 1  # since each char is a palindrome
    dp = [[False for _ in range(n)] for _ in range(n)]

    # base cases
    for i in range(n):
        dp[i][i] = True

    # iteration
    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n):
            if st[start] == st[end]:
                # if the string consists of only two letters or remaining string is palindromic
                if end-start == 1 or dp[start + 1][end - 1]:
                    dp[start][end] = True
                    max_len = max(max_len, end - start + 1)

    return max_len


# Optimized dp
# Time: O(n**2) | Space: O(n)
def find_LPS_length(st):
    if not st:
        return False

    # init vars
    n = len(st)
    max_len = 1  # since each char is a palindrome
    dp = [[False for _ in range(n)] for _ in range(2)]

    # base cases
    for i in range(n):
        dp[i % 2][i] = True

    # iteration
    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n):
            if end-start == 1 or st[start] == st[end]:
                if dp[(start + 1) % 2][end - 1]:
                    dp[start % 2][end] = True
                    max_len = max(max_len, end - start + 1)

    return max_len


def main():
    print(find_LPS_length("abdbca"))
    print(find_LPS_length("cddpd"))
    print(find_LPS_length("pqr"))


if __name__ == '__main__':
    main()
