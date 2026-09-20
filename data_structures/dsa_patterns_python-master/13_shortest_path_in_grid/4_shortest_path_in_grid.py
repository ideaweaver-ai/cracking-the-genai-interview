# Copyright © 2020 way2FAANG

# LeetCode: 1091

from collections import deque
from typing import List


class Solution:
    # Time: O(r*c) | Space: O(r*c) additional space for queue
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:

        # Input validation
        if not grid or grid[0][0] == 1:  # left corner blocked
            return -1

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # Output var
        shortest_path_dist = 0

        # Initialize BFS queue and add left corner
        queue = deque()
        grid[0][0] = 1  # imp - dont forget to mark (0, 0) visited
        queue.append([0, 0])

        # BFS
        while queue:
            # since we need distance in each iteration we should cover nodes level by level
            level_size = len(queue)
            shortest_path_dist += 1

            for _ in range(level_size):
                # current_node
                i, j = queue.popleft()
                # If we reached right bottom corner - return
                if i == rows - 1 and j == cols - 1:
                    return shortest_path_dist

                neighbors = [[i + 1, j],
                             [i - 1, j],
                             [i, j + 1],
                             [i, j - 1],
                             [i + 1, j + 1],
                             [i + 1, j - 1],
                             [i - 1, j + 1],
                             [i - 1, j - 1]]

                for r, c in neighbors:
                    # validate neighbors
                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                        # mark this cell visited - make it 1
                        # any path reahcing this cell after this will have larger distance
                        grid[r][c] = 1
                        queue.append([r, c])

        return -1


if __name__ == '__main__':
    grid = [[0, 1], [1, 0]]
    sol = Solution()
    print(sol.shortestPathBinaryMatrix(grid))

    grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    sol = Solution()
    print(sol.shortestPathBinaryMatrix(grid))
