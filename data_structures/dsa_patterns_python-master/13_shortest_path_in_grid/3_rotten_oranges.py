# Copyright © 2020 way2FAANG

# LeetCode: 994

from collections import deque
from typing import List


class Solution:
    # Time: O(r*c) | Space: O(r*c) additional space for queue
    def orangesRotting(self, grid: List[List[int]]) -> int:

        # Input validation
        if not grid:
            return 0

        # output var
        mins = 0
        fresh_oranges = 0  # we need to return mins only if all oranges get rotten

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # define queue
        # add initial nodes to queue - cells with value 2
        queue = deque()
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:
                    queue.append([i, j])
                elif grid[i][j] == 1:
                    fresh_oranges += 1

        # No need for visited as we are going to check if cell is 1 and only then coner it and add it to queue

        # required for case - [[0]] we will return -1 but it should be 0
        if fresh_oranges == 0:
            return 0

        # BFS
        while queue:
            # since we need to capture mins, we need level size
            level_size = len(queue)
            mins += 1

            for _ in range(level_size):
                # deque current node
                i, j = queue.popleft()

                neighbors = [[i + 1, j],
                                       [i - 1, j],
                                       [i, j + 1],
                                       [i, j - 1]]

                for r, c in neighbors:
                    # validate neighbors
                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                        # convert he orange to rotten
                        grid[r][c] = 2
                        # reduce count of fresh oranges
                        fresh_oranges -= 1

                        # add it to bfs queue
                        queue.append([r, c])

        # why return mins-1?
        # ans lies in when do we exit bfs queue?
        # in the last level iteration of bfs queue, we don't add any valid neighbors
        # means in the last iteration of bfs queue we will always have only rotten oranges
        # hence we exit in next iteration
        # since we have to return mins to rot, we should return mins-1
        return -1 if fresh_oranges != 0 else mins-1


if __name__ == '__main__':
    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    sol = Solution()
    print(sol.orangesRotting(grid))

    grid = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
    sol = Solution()
    print(sol.orangesRotting(grid))
