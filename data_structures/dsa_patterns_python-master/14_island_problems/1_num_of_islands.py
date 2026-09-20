# Copyright © 2020 way2FAANG

# LeetCode: 200
from typing import List


# Time: O(r*c) time | Space: O(r*c) - for function stack in recursion
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        # dfs helper defined as inner function to prevent passing parameters
        def dfs(i, j):
            # Mark visited - since we are marking visited and we check while calling dfs, no other base case required
            grid[i][j] = '0'  # check if you understand

            neighbors = [[i + 1, j],
                         [i - 1, j],
                         [i, j + 1],
                         [i, j - 1]]

            for r, c in neighbors:
                # validate neighbors
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1':
                    dfs(r, c)

        # Input validation
        if not grid:
            return 0

        # Output var
        num_islands = 0

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # Iterate through each cell
        # whenever you find , use dfs to cover the island
        # Increase count of islands
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '1':
                    num_islands += 1
                    dfs(i, j)

        # Return
        return num_islands

    # DFS iterative - using stack, convert recursive code to stack
    def numIslands(self, grid: List[List[str]]) -> int:

        # Input validation
        if not grid:
            return 0

        # Output var
        num_islands = 0

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # stack for dfs
        stack = []

        # Iterate through each cell
        # whenever you find , use dfs to cover the island
        # Increase count of islands
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '1':
                    num_islands += 1

                    # DFS iterative through stack
                    stack.append([i, j])
                    # ** v imp - different from recursive
                    # mark visited when adding to stack
                    grid[i][j] = 0

                    while stack:
                        # current node
                        x, y = stack.pop()
                        potential_neighbors = [[x + 1, y],
                                               [x - 1, y],
                                               [x, y + 1],
                                               [x, y - 1]]

                        for r, c in potential_neighbors:
                            # validate neighbors
                            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1':
                                stack.append([r, c])
                                # ** v imp - mark visited when adding
                                grid[r][c] = 0

        # Return
        return num_islands


if __name__ == '__main__':
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    sol = Solution()
    print(sol.numIslands(grid))
