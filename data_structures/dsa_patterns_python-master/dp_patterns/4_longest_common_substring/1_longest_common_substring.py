def find_LCS_length(s1, s2):
    # BF
    # Time: O(3**(m+n)) | Space: O(m+n)
    def find_LCS_length_helper(i1, i2, count):
        # base cases
        if i1 == len(s1) or i2 == len(s2):
            return 0
        # recursion
        if s1[i1] == s2[i2]:
            count = find_LCS_length_helper(i1 + 1, i2 + 1, count + 1)

        count1 = find_LCS_length_helper(i1, i2 + 1, 0)
        count2 = find_LCS_length_helper(i1 + 1, i2, 0)
        return max(count, max(count1, count2))

    # main function
    return find_LCS_length_helper(0, 0, 0)


# Memoized version
def find_LCS_length(s1, s2):
    # Memoized
    # Time: O((m*n*(m+n) | Space: O(m+n)
    def find_LCS_length_helper(i1, i2, count, memo={}):
        # base cases
        if i1 == len(s1) or i2 == len(s2):
            return 0
        # memo check
        if (i1, i2) in memo:
            return memo[(i1, i2)]
        # recursion
        if s1[i1] == s2[i2]:
            count = find_LCS_length_helper(i1 + 1, i2 + 1, count + 1)

        count1 = find_LCS_length_helper(i1, i2 + 1, 0)
        count2 = find_LCS_length_helper(i1 + 1, i2, 0)
        memo[(i1, i2, count)] = max(count, max(count1, count2))
        return memo[(i1, i2, count)]

    # main function
    return find_LCS_length_helper(0, 0, 0)


def find_LCS_length(s1, s2):
    # BF
    # Time: O(3**(m+n)) | Space: O(m+n)
    def find_LCS_length_helper(i1, i2, count, memo={}):
        # base cases
        if i1 == len(s1) or i2 == len(s2):
            return 0
        # memo check
        if (i1, i2) in memo:
            return memo[(i1, i2)]
        # recursion
        if s1[i1] == s2[i2]:
            count = find_LCS_length_helper(i1 + 1, i2 + 1, count + 1)

        count1 = find_LCS_length_helper(i1, i2 + 1, 0)
        count2 = find_LCS_length_helper(i1 + 1, i2, 0)
        memo[(i1, i2, count)] = max(count, max(count1, count2))
        return memo[(i1, i2, count)]

    # main function
    return find_LCS_length_helper(0, 0, 0)


def main():
    print(find_LCS_length("abdca", "cbda"))
    print(find_LCS_length("passport", "ppsspt"))


if __name__ == "__main__":
    main()
