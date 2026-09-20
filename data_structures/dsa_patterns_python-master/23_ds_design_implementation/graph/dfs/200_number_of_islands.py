from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        def get_valid_neighbors(i, j):

            potential_neighbors = [[i, j + 1], [i, j - 1], [i + 1, j], [i - 1, j]]
            valid_neighbors = []

            for r, c in potential_neighbors:
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1':
                    valid_neighbors.append([r, c])

            return valid_neighbors

        def dfs_helper(i, j):

            # mark the cell visited
            # Can do this because in dfs we cover all connected 1s in one base dfs iteration
            grid[i][j] = 0
            # adding only cells with values 1 this should take care, no need for base case
            for r, c in get_valid_neighbors(i, j):
                dfs_helper(r, c)

        ## Main function
        if not grid:
            return 0

        # get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # counting number of islands
        num_of_islands = 0

        for i in range(rows):
            for j in range(cols):
                # Whenever you find a land, cover all connected 1's and that will be 1 island
                if grid[i][j] == '1':
                    num_of_islands += 1
                    dfs_helper(i, j)

        return num_of_islands

# DFS iterative - converted recursive code to iterative through stack
# same time complexity and space complexity
# class Solution:
#     # DFS iterative - using stack, convert recursive code to stack
#     def numIslands(self, grid: List[List[str]]) -> int:
#
#         # Input validation
#         if not grid:
#             return 0
#
#         # Output var
#         num_islands = 0
#
#         # Get rows and cols
#         rows = len(grid)
#         cols = len(grid[0])
#
#         # stack for dfs
#         stack = []
#
#         # Iterate through each cell
#         # whenever you find , use dfs to cover the island
#         # Increase count of islands
#         for i in range(rows):
#             for j in range(cols):
#                 if grid[i][j] == '1':
#                     num_islands += 1
#                     # DFS iterative through stack
#                     stack.append([i, j])
#                     while stack:
#                         # current node
#                         x, y = stack.pop()
#                         # mark visited
#                         grid[x][y] = '0'
#                         potential_neighbors = [[x + 1, y],
#                                                [x - 1, y],
#                                                [x, y + 1],
#                                                [x, y - 1]]
#
#                         for r, c in potential_neighbors:
#                             # validate neighbors
#                             if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1':
#                                 stack.append([r, c])
#
#         # Return
#         return num_islands


if __name__ == '__main__':
    grid = [ ['1', '1', '0', '0', '0'],
             ['1', '1', '0', '0', '0'],
             ['0', '0', '1', '0', '0'],
             ['0', '0', '0', '1', '1']]
    sol = Solution()
    print(sol.numIslands(grid))
