from collections import deque
from typing import List


# class Solution:
#
#     # BFS with visited
#     # O(N) time (since max neighbors - 8 which is constant) , O(N) space
#     def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
#
#         # inner function so don't have to pass grid parameters
#         # In variations - mostly you will have to modify this function
#         def get_valid_neighbors(cell_row, cell_column):
#             potential_neighbors = [[cell_row, cell_column + 1], [cell_row + 1, cell_column + 1],
#                                    [cell_row + 1, cell_column], [cell_row + 1, cell_column - 1],
#                                    [cell_row, cell_column - 1], [cell_row - 1, cell_column - 1],
#                                    [cell_row - 1, cell_column], [cell_row - 1, cell_column + 1],
#                                    ]
#             valid_neighbors = []
#             for row, column in potential_neighbors:
#                 if 0 <= row < rows and 0 <= column < columns and grid[row][column] == 0 and visited[row][column] is False:
#                     valid_neighbors.append([row, column])
#             return valid_neighbors
#
#         ## Main function
#         # Input validation check if root is blocked:
#         if grid[0][0]:
#             return -1
#
#         # Number of rows, columns of grid
#         rows = len(grid)
#         columns = len(grid[0])
#
#         # Since a node of graph has multiple incoming edges and cycles we need to maintain visited
#         visited = [[False for _ in range(columns)] for _ in range(rows)]
#
#         # BFS queue, add source and path length
#         queue = deque()
#         queue.append((0, 0, 1))  # source_row, source_column, count_of_nodes_on_path
#         # Mark a node visited when adding to the queue
#         visited[0][0] = True
#
#         while queue:
#             current_row, current_column, path_length = queue.popleft()
#
#             # Check if destination
#             if current_row == rows - 1 and current_column == columns - 1:
#                 return path_length
#
#             # Add valid neighbors to queue - in tree we added left and right children
#             for neigbor_row, neighbor_col in get_valid_neighbors(current_row, current_column):
#                 queue.append((neigbor_row, neighbor_col, path_length + 1))
#                 # Mark a node visited when adding to the queue
#                 visited[neigbor_row][neighbor_col] = True
#
#         return -1
#
#     BFS without visited - change the matrix
#     O(N) time (since max neighbors - 8 which is constant) , O(N) space

class Solution:

    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        # Input validation
        if not grid or grid[0][0] == 1:  # left corner blocked
            return -1

        # Output var
        dist = 0

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # Initialize BFS queue and add left corner
        queue = deque()
        queue.append([0, 0, 1])  # need to add dist in this case

        # BFS
        while queue:
            # Get current node
            i, j, dist = queue.popleft()

            # If we reached right bottom corner - return
            if i == rows - 1 and j == cols - 1:
                return dist  # distance of current node

            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1],
                                   [i + 1, j + 1],
                                   [i + 1, j - 1],
                                   [i - 1, j + 1],
                                   [i - 1, j - 1]]

            for r, c in potential_neighbors:
                # validate neighbors
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                    # mark this cell visited - make it 1. because any path reahcing this cell after this will have larger distance
                    grid[r][c] = 1
                    queue.append([r, c, dist + 1])

        return -1


if __name__ == '__main__':
    grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    solution = Solution()
    print(solution.shortestPathBinaryMatrix(grid))