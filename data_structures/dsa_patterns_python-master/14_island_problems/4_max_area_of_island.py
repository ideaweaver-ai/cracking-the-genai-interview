# Copyright © 2020 way2FAANG

# LeetCode: 695
from typing import List

# Look at the code - This code solves the question with perfect TC & SC but is not great ???
# Because we define current_area as instance var, it can essentially run as a single threaded execution from the same objet
# to run multi threaded - we need to create one object per thread
# Time: O(r*c) | Space: O(r*c)
class Solution:
    def __init__(self):
        # Output var - since we need to update global variable
        # define it as an instance var
        self.max_area = 0

        # defining current area as instance var
        self.current_area = 0

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:

        def dfs_helper(i, j):
            # mark visited
            grid[i][j] = 0

            # increase current_area
            self.current_area += 1

            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            for r, c in potential_neighbors:
                # validate neighbors
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                    # if we had not defined current_area as instance var
                    # all neighbors would have got current_area var of parent - which is wrong
                    dfs_helper(r, c)

        # Input validation
        if not grid:
            return 0

        # Get num of rows and columns
        rows = len(grid)
        cols = len(grid[0])

        # Iterate through each cell of grid
        # When you find land, cover the entire island through dfs
        # COunt area and max area
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    # everytime a new island is found initialize area as 0
                    self.current_area = 0
                    dfs_helper(i, j)
                    # max area can also be updated inside dfs, but instead of updating max area every time inside dfs
                    # we can do it once when we have done dfs for the entire island
                    # update max area
                    self.max_area = max(self.max_area, self.current_area)

        return self.max_area

# Better approach for multithreading
class Solution:
    def __init__(self):
        # Output var - since we need to update global variable
        # define it as an instance var
        self.max_area = 0

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:

        def dfs_helper(i, j, current_area):
            # mark visited
            grid[i][j] = 0

            # increase current_area
            current_area += 1

            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            for r, c in potential_neighbors:
                # validate neighbors
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                    # if we had not defined current_area as instance var
                    # all neighbors would have got current_area var of parent - which is wrong
                    current_area = dfs_helper(r, c, current_area)

            return current_area

        # Input validation
        if not grid:
            return 0

        # Get num of rows and columns
        rows = len(grid)
        cols = len(grid[0])

        # Iterate through each cell of grid
        # When you find land, cover the entire island through dfs
        # Count area and max area
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    # everytime a new island is found initialize area as 0
                    self.current_area = 0
                    current_area_island = dfs_helper(i, j, 0)
                    # max area can also be updated inside dfs, but instead of updating max area every time inside dfs
                    # we can do it once when we have done dfs for the entire island
                    # update max area
                    self.max_area = max(self.max_area, current_area_island)

        return self.max_area


# Stack - iterative soln
# # O(r*c) time | O(r*c) space
# class Solution:
#     def __init__(self):
#         # Output var - since we need to update global variable
#         # define it as an instance var
#         self.max_area = 0
#         # Don't need to define current_area as instance var for iterative sol
#
#     # DFS - iterative through stack
#     def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
#
#         # Input validation
#         if not grid:
#             return 0
#
#         # Get num of rows and columns
#         rows = len(grid)
#         cols = len(grid[0])
#
#         # DFS stack
#         stack = []
#
#         # Iterate through each cell of grid
#         # When you find land, cover the entire island through dfs
#         # Count area and update max area
#         for i in range(rows):
#             for j in range(cols):
#                 if grid[i][j] == 1:
#
#                     # everytime a new island is found initialize area as 0
#                     current_area = 0
#                     stack.append([i, j])
#                     # **v imp
#                     # we can mark visited when we add to stack or pop from stack
#                     # if we mark visited when popping the node, we can have double counting
#                     # take example grid = [[1, 1], [1, 1]];  when [0,0] processed it adds [1, 0] and [0, 1] to stack.
#                     # Now [0,1] will add [1, 1] and [1,1] will add [1, 0] which is double counting [1,0] as it was not marked visited
#                     # Again notice this is happening because stack is LIFO
#                     # so best way (either using stack for dfs or queue for bfs) to mark a node visited when added to stack
#                     grid[i][j] = 0
#
#                     while stack:
#                         x, y = stack.pop()
#                         # increase area and update max
#                         current_area += 1
#                         self.max_area = max(self.max_area, current_area)
#
#                         # Add valid neighbors to stack
#                         potential_neighbors = [[x + 1, y],
#                                                [x - 1, y],
#                                                [x, y + 1],
#                                                [x, y - 1]]
#
#                         for r, c in potential_neighbors:
#                             # Validate neighbors
#                             if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
#                                 stack.append([r, c])
#                                 # mark visited - ** vimp, different from recursin dfs
#                                 grid[r][c] = 0
#
#         return self.max_area


if __name__ == '__main__':
    grid = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]
    sol = Solution()
    print(sol.maxAreaOfIsland(grid))
