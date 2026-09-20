from typing import List


class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:

        def dfsHelper(i, j):
            # Since we started dfs it is an island
            # SO either it could be closed (surrounded everywhere with water) or it is connected to an edge of grid - in which case it is not closed
            if i < 0 or i >= rows or j < 0 or j >= cols:
                return False

            # base case - if we reach water - this cell is closed
            if grid[i][j] == 1:
                return True

            # mark visited
            grid[i][j] = 1

            up = dfsHelper(i - 1, j)
            down = dfsHelper(i + 1, j)
            left = dfsHelper(i, j - 1)
            right = dfsHelper(i, j + 1)

            return up and down and left and right

        # Number of rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # Output var
        num_closed_islands = 0

        # Find land(0) and do dfs to cover the island
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 0 and dfsHelper(i, j):  # perform dfs and return True if closed island
                    num_closed_islands += 1

        return num_closed_islands