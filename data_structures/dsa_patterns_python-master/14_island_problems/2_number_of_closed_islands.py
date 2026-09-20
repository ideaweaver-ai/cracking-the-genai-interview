# Copyright © 2020 way2FAANG

# LeetCode: 1254
from typing import List


# Time: O(r*c) | Space: O(r*c)
class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        # Define dfs helper as inner function to prevent passing params
        def dfs(i, j):
            # If reached water - return true
            if grid[i][j] == 1:
                return True

            # If reached an edge - return False
            if i - 1 < 0 or i + 1 >= rows or j - 1 < 0 or j + 1 >= cols:
                return False

            # Mark visited - make it water
            grid[i][j] = 1

            # is_closed_island = True

            # neighbor = [[i + 1, j],
            #             [i - 1, j],
            #             [i, j + 1],
            #             [i, j - 1]]
            #
            # for r, c in neighbor:
            #     if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
            #         is_closed_island &= dfs(r, c)
            #
            # return is_closed_island

            is_bottom_closed = dfs(i + 1, j)
            is_top_closed = dfs(i - 1, j)
            is_right_closed = dfs(i, j + 1)
            is_left_closed = dfs(i, j - 1)

            return is_bottom_closed and is_top_closed and is_right_closed and is_left_closed



        # Input validation
        if not grid:
            return 0

        # Output var
        num_closed_islands = 0

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # Iterate through each cell
        # Whenever we find land(0), cover the entire island (dfs) and check if its closed
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 0:
                    if dfs(i, j):
                        # starting dfs on a land cell either you can reach an edge
                        # or it will be a closed island
                        num_closed_islands += 1

        return num_closed_islands


if __name__ == '__main__':
    grid = [[0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0]]
    sol = Solution()
    print(sol.closedIsland(grid))
