def find_minimum_deletions(st):
    # init vars
    n = len(st)
    dp = [[0 for _ in range(n)] for _ in range(n)]
    max_len = 1

    # base cases
    for i in range(n):
        dp[i][i] = 1

    # dp
    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n):
            if st[start] == st[end]:
                dp[start][end] = 2 + dp[start + 1][end - 1]
            else:
                dp[start][end] = max(dp[start + 1][end], dp[start][end - 1])
            max_len = max(max_len, dp[start][end])

    return n - max_len


def main():
    print(find_minimum_deletions("abdbca"))
    print(find_minimum_deletions("cddpd"))
    print(find_minimum_deletions("pqr"))


if __name__ == "__main__":
    main()
