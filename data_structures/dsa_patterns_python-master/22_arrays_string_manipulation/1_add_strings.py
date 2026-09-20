# Copyright © 2020 way2FAANG
# LeetCode: 642


class Solution:
    # Time: O(max(len(num1), len(num2))) | Space: O(max(len(num1), len(num2)))
    def addStrings(self, num1: str, num2: str) -> str:
        p1, p2 = len(num1) - 1, len(num2) - 1
        # total_sum = 0
        # since we don't want to use the inbuilt str function, better we use array for result
        result = []
        carry = 0
        # multiplier = 1

        while p1 >= 0 or p2 >= 0:
            # add last digit and update carry
            v1 = ord(num1[p1]) - ord('0') if p1 >= 0 else 0
            v2 = ord(num2[p2]) - ord('0') if p2 >= 0 else 0

            digit_sum = (v1 + v2 + carry) % 10
            carry = (v1 + v2 + carry) // 10

            # update result
            result.append(digit_sum)
            # total_sum += digit_sum*multiplier
            # multiplier *= 10

            # update poineters
            p1 -= 1
            p2 -= 1

        if carry:
            # total_sum += carry*multiplier
            result.append(carry)

        # reverse and convert individual element to str
        result = [str(n) for n in result[::-1]]

        return "".join(result)