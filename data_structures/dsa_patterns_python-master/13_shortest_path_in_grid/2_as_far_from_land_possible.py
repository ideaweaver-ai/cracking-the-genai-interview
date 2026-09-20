# Copyright © 2020 way2FAANG

# LeetCode: 1162
from collections import deque
from typing import List


class Solution:
    # Time: O(r*c) | Space: O(r*c) additional space for queue
    def maxDistance(self, grid: List[List[int]]) -> int:

        # Get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # output vars
        max_dist = -1
        # initialized inf since we need to update dist from nearest land cell
        dist = [[float('inf') for _ in range(cols)] for _ in range(rows)]

        # Don't need visited flag as we are going to check and add only those cells whose distance is updated

        # Initialize bfs queue
        # As 1's determine the dist from land, add 1's to the queue
        queue = deque()
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    # for a land cell dist to nearest land cell is 0
                    dist[i][j] = 0
                    queue.append([i, j])

        # Perform bfs
        while queue:
            # current node
            i, j = queue.popleft()

            neighbors = [[i + 1, j],
                         [i - 1, j],
                         [i, j + 1],
                         [i, j - 1]]

            for r, c in neighbors:
                # we dont need visited ?
                # since we check if the current dist is > then dist from i,j cell and only then update
                # validate neighbors
                if 0 <= r < rows and 0 <= c < cols and dist[i][j] + 1 < dist[r][c]:
                    dist[r][c] = dist[i][j] + 1  # update dist
                    queue.append([r, c])  # potentially this cell could update dist of its neighbors
                    # update max dist till now - we can do this because of bfs
                    # the first time the update happens is the min dist for that cell from land 1
                    max_dist = max(max_dist, dist[r][c])

        return max_dist


if __name__ == '__main__':
    # Test case 1
    grid = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    sol = Solution()
    print(sol.maxDistance(grid))

    # Test case 2
    grid = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    sol = Solution()
    print(sol.maxDistance(grid))
