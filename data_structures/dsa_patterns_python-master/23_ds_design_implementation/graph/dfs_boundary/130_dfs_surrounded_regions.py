from itertools import product
from typing import List

from itertools import product
from collections import deque


# BFS solution
# O(n) time (Each cell is visited twice worst case) | O(n) space for stack
# class Solution:
#     def solve(self, board: List[List[str]]) -> None:
#         """
#         Do not return anything, modify board in-place instead.
#         """
#
#         def bfs(i, j):
#             # Create BFS queue
#             queue = deque()
#
#             # Add to queue and mark visited
#             queue.append([i, j])
#             board[i][j] = 'e'
#
#             while queue:
#                 # pop current node
#                 i, j = queue.popleft()
#
#                 potential_neighbors = [[i + 1, j],
#                                        [i - 1, j],
#                                        [i, j + 1],
#                                        [i, j - 1]]
#
#                 # validate neighbors and add to queue
#                 for r, c in potential_neighbors:
#                     if 0 <= r < rows and 0 <= c < cols and board[r][c].lower() == 'o':
#                         queue.append([r, c])
#                         # mark visited
#                         board[r][c] = 'e'
#
#         # main function
#         # Validate Input
#         if not board:
#             return board
#
#         # Get rows and cols
#         rows = len(board)
#         cols = len(board[0])
#
#         # Find 'o' in the border
#         # Perform dfs to find connected 'o's
#         # Mark them so they are not changed
#         border = list(product([0, rows - 1], range(cols))) + list(product(range(rows), [0, cols - 1]))
#
#         for i, j in border:
#             # print(board[i][j])
#             if board[i][j].lower() == 'o':
#                 bfs(i, j)
#
#         # Iterate through all the elements and capture non border o's
#         for i in range(rows):
#             for j in range(cols):
#                 if board[i][j].lower() == 'o':
#                     board[i][j] = 'X'
#                 elif board[i][j].lower() == 'e':
#                     board[i][j] = 'O'


# DFS solution
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        # Define dfs as inner func to avoid passing all parameters
        def dfs_helper(i, j):
            # mark visited
            # we need to differentiate border connected o's from other o's
            # better to mark in place instead of using visited flag

            board[i][j] = 'e'

            # potetntial neigbors
            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            for r, c in potential_neighbors:
                if 0 <= r < rows and 0 <= c < cols and board[r][c].lower() == 'o':
                    dfs_helper(r, c)

        if not board:
            return board

        # Get rows and cols
        rows = len(board)
        cols = len(board[0])

        # Find 'o' in the border
        # Perform dfs to find connected 'o's
        # Mark them so they are not changed
        border = list(product([0, rows - 1], range(cols))) + list(product(range(rows), [0, cols - 1]))

        for i, j in border:
            # print(board[i][j])
            if board[i][j].lower() == 'o':
                dfs_helper(i, j)

        # Iterate through all the elements and capture non border o's
        for i in range(rows):
            for j in range(cols):
                if board[i][j].lower() == 'o':
                    board[i][j] = 'X'
                elif board[i][j].lower() == 'e':
                    board[i][j] = 'O'


from itertools import product
from collections import deque

# DFS solution - with stack (order will not be same as dfs recursive) -  1 line change from bfs
# O(n) time (Each cell is visited twice worst case) | O(n) space for stack
# class Solution:
#     def solve(self, board: List[List[str]]) -> None:
#         """
#         Do not return anything, modify board in-place instead.
#         """
#
#         def dfs(i, j):
#             # Create DFS stack
#             stack = []
#
#             # Add to queue and mark visited
#             stack.append([i, j])
#             board[i][j] = 'e'
#
#             while stack:
#                 # pop current node
#                 i, j = stack.pop()
#
#                 potential_neighbors = [[i + 1, j],
#                                        [i - 1, j],
#                                        [i, j + 1],
#                                        [i, j - 1]]
#
#                 # validate neighbors and add to queue
#                 for r, c in potential_neighbors:
#                     if 0 <= r < rows and 0 <= c < cols and board[r][c].lower() == 'o':
#                         stack.append([r, c])
#                         # mark visited
#                         board[r][c] = 'e'
#
#         # main function
#         # Validate Input
#         if not board:
#             return board
#
#         # Get rows and cols
#         rows = len(board)
#         cols = len(board[0])
#
#         # Find 'o' in the border
#         # Perform dfs to find connected 'o's
#         # Mark them so they are not changed
#         border = list(product([0, rows - 1], range(cols))) + list(product(range(rows), [0, cols - 1]))
#
#         for i, j in border:
#             # print(board[i][j])
#             if board[i][j].lower() == 'o':
#                 dfs(i, j)
#
#         # Iterate through all the elements and capture non border o's
#         for i in range(rows):
#             for j in range(cols):
#                 if board[i][j].lower() == 'o':
#                     board[i][j] = 'X'
#                 elif board[i][j].lower() == 'e':
#                     board[i][j] = 'O'

sol = Solution()
board = [["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]
sol.solve(board)
print(board)  # since board is modified inplace
