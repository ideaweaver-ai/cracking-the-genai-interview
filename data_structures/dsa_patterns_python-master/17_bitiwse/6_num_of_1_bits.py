# Copyright © 2020 way2FAANG
# LeetCode: 191


class Solution:
    # Time: O(b) - b is num of bits | Space: O(1)
    def hammingWeight(self, n: int) -> int:
        num_of_one_bits = 0
        while n:
            if n & 1:
                num_of_one_bits += 1  # get the least significant bit (1 or 0)
            n = n >> 1

        return num_of_one_bits


if __name__ == '__main__':
    sol = Solution()
    print(sol.hammingWeight(15))
