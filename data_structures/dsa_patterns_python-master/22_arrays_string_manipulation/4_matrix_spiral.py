# Copyright © 2020 way2FAANG
# LeetCode: 54

from typing import List


class Solution:
    # Time: O(n) | Space: O(n) - for visited
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        # Input validation
        if not matrix:
            return []

        # Get rows and cols
        rows = len(matrix)
        cols = len(matrix[0])

        # Visited flag
        # visited =  [[False for _ in range(cols)] for _ in range(rows)]
        # no need for visited flag. We will change visited cell to an invalid value

        # output var
        result = []

        # shift
        shift = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        # Start row, col and direction index
        r, c, di = 0, 0, 0

        for _ in range(rows):
            for _ in range(cols):
                # Append to result and mark seen
                result.append(matrix[r][c])
                # Mark visited
                matrix[r][c] = -101

                # Calculate next cell
                new_r = r + shift[di][0]  # x shift
                new_c = c + shift[di][1]  # y shift

                if new_r not in range(rows) or new_c not in range(cols) or matrix[new_r][
                    new_c] == -101:  # all visited cells are -101
                    di = (di + 1) % 4
                    new_r = r + shift[di][0]  # x shift
                    new_c = c + shift[di][1]  # y shift

                # guaranteed to have a valid cell coordinate
                r = new_r
                c = new_c

        return result
