# Top down DP
# Time: O(n**2) | Space: O(n**2)
def find_LPS_length(st):
    if not st:
        return 0

    # init vars
    n = len(st)
    count = 0  # since each char is a palindrome
    dp = [[False for _ in range(n)] for _ in range(n)]

    # base cases
    for i in range(n):
        dp[i][i] = True
        count += 1

    # iteration
    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n):
            if st[start] == st[end]:
                # if the string consists of only two letters or remaining string is palindromic
                if end - start == 1 or dp[start + 1][end - 1]:
                    dp[start][end] = True
                    count += 1
    return count


# Optimized dp
# Time: O(n**2) | Space: O(n)
def find_LPS_length(st):
    if not st:
        return 0

    # init vars
    n = len(st)
    count = 0  # since each char is a palindrome
    dp = [[False for _ in range(n)] for _ in range(2)]

    # base cases
    for i in range(n):
        dp[i%2][i] = True
        count += 1

    # iteration
    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n):
            if st[start] == st[end]:
                # if the string consists of only two letters or remaining string is palindromic
                if end - start == 1 or dp[(start + 1) % 2][end - 1]:
                    dp[start % 2][end] = True
                    count += 1
    return count


def main():
    print(find_LPS_length("abdbca"))
    print(find_LPS_length("cddpd"))
    print(find_LPS_length("pqr"))


if __name__ == '__main__':
    main()
