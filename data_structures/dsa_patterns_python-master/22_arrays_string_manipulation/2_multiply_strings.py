# Copyright © 2020 way2FAANG
# LeetCode: 43
# Level: Medium
# ** - good problem

class Solution:
    # Time: O(n1+n2) | SPace: O(n1+n2)
    def multiply(self, num1: str, num2: str) -> str:
        n1, n2 = len(num1), len(num2)
        result = [0 for _ in range(n1 + n2)]

        for i in range(-1, -n1 - 1, -1):
            for j in range(-1, -n2 - 1, -1):
                # instead of handling quotient, remainder at both multiplication and sum level
                # add product directly to correct digit and hadle quotient and remainder
                result[i + j + 1] += int(num1[i]) * int(num2[j])
                # first add carry to previous digit - else we will losse it
                result[i + j] += result[i + j + 1] // 10
                result[i + j + 1] %= 10

                # find number of leading zeros
        p_zeros = 0
        # imp - we need to remove only trailing zeros - go only until second last digit
        # else we will remove last zero also in cases where the result is acutally 0
        while p_zeros < len(result) - 1 and result[p_zeros] == 0:
            p_zeros += 1

        result = "".join(map(str, result[p_zeros:]))
        return result
