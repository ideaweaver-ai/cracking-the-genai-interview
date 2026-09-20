# Copyright © 2020 way2FAANG

# LeetCode: 694
from typing import List


# Time: O(r*c) | Space: O(r*c)

class Solution:
    def numDistinctIslands(self, grid: List[List[int]]) -> int:

        def dfs_helper(i, j, direction, current_shape):
            # mark visited
            grid[i][j] = 0

            # add current direction to current_shape
            current_shape.append(direction)

            potential_neighbors = [[i, j + 1, 1],  # coordinates and direction
                                   [i, j - 1, 2],
                                   [i + 1, j, 3],
                                   [i - 1, j, 4]]

            for r, c, d in potential_neighbors:
                # validate neighbors
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                    dfs_helper(r, c, d, current_shape)

            # imp- ele we will confuse
            # Try this test case - [[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]
            current_shape.append(0)  # for end of each path

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # output var
        shapes = set()  # since we need islands only with different shapes

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    # land found - covert he island by dfs
                    current_shape = []
                    dfs_helper(i, j, 0, current_shape)  # start and end directions - 0
                    print(current_shape)
                    shapes.add(tuple(current_shape))  # list cannot be added to set as it is mutable

        return len(shapes)


if __name__ == '__main__':
    grid = [[1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [1, 1, 0, 1, 1]]
    sol = Solution()
    print(sol.numDistinctIslands(grid))
