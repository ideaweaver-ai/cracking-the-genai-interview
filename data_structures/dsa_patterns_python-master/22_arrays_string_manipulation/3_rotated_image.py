# Copyright © 2020 way2FAANG
# LeetCode: 48

from typing import List


class Solution:
    # Time: O(n) | Space: O(1)
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        for i in range(n // 2):
            for j in range(i, n - 1 - i):
                # matrix[i][j], matrix[~j][i], matrix[~i][~j], matrix[j][~i] = matrix[~j][i], matrix[~i][~j], matrix[j][~i], matrix[i][j]
                matrix[j][n-1-i], matrix[n-1-i][n-1-j], matrix[n-1-j][i], matrix[i][j] = \
                    matrix[i][j], matrix[j][n-1-i], matrix[n-1-i][n-1-j], matrix[n-1-j][i]
        return matrix


if __name__ == "__main__":
    sol = Solution()
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(sol.rotate(matrix))
    matrix = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    print(sol.rotate(matrix))
