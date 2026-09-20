from collections import deque
from typing import List


class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:

        def getValidNeighbors(i, j):
            potential_neighbors = [[i, j + 1], [i + 1, j], [i, j - 1], [i - 1, j]]
            valid_neighbors = []
            for r, c in potential_neighbors:
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0 and not visited[r][c]:
                    valid_neighbors.append([r, c])
            return valid_neighbors

        # get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # Out vars
        # dist = [[ -float('inf') for _ in range(cols)] for _ in range(rows)]
        # We can use a dist matrix or add dist in que as we don't need to return dist
        max_dist = -1

        # Define visited
        visited = [[False for _ in range(cols)] for _ in range(rows)]

        # Define Bfs queue
        que = deque()

        # Populate queue - with 1's
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    que.append([i, j, 0])  # cell coordinates, distance
                    visited[i][j] = True

        while que:
            i, j, dist = que.popleft()
            for r, c in getValidNeighbors(i, j):
                visited[r][c] = 1
                max_dist = max(max_dist, dist + 1)
                que.append([r, c, dist + 1])

        return max_dist


if __name__ == '__main__':
    grid = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    solution = Solution()
    print(solution.maxDistance(grid))
