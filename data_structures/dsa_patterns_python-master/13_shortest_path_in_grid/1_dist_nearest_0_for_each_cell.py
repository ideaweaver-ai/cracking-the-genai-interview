# Copyright © 2020 way2FAANG
# LeetCode: 542

from typing import List
from collections import deque


# Brute force
# Time: O(r*c)**2 | Space: O(1) excluding o/p (no additional space), O(r*c) including o/p
class Solution:

    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        # get rows & columns
        rows = len(matrix)
        columns = len(matrix[0])
        # while creating multidimensinal arrays got last dimension to first dimension
        dist = [[float('inf') for _ in range(columns)] for _ in range(rows)]

        for i in range(rows):
            for j in range(columns):
                if matrix[i][j] == 0:
                    dist[i][j] = 0
                else:
                    for l in range(rows):
                        for k in range(columns):
                            if matrix[l][k] == 0:
                                current_dist = abs(l-i) + abs(k-j)
                                dist[i][j] = min(dist[i][j], current_dist)
        return dist


class Solution:
    # Time: O(r*c) | Space: O(r*c) additional space for queue
    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:

        # Get rows and cols
        rows = len(matrix)
        cols = len(matrix[0])

        # Output var
        # while creating multidimensinal arrays go last dimension to first dimension
        dist = [[float('inf') for i in range(cols)] for j in range(rows)]

        # Cells which are 0 have their distance 0 and need to be added to BFS
        queue = deque()
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    dist[i][j] = 0
                    queue.append([i, j])

        # BFS
        while queue:
            # no need for visited, as we are going to check if the min dist is getting updated
            # and only then add that cell to the queue
            i, j = queue.popleft()  # current node

            neighbors = [[i + 1, j],
                         [i - 1, j],
                         [i, j + 1],
                         [i, j - 1]]

            for r, c in neighbors:
                # check valid neighbors and if distance is getting updated
                if 0 <= r < rows and 0 <= c < cols and dist[i][j] + 1 < dist[r][c]:
                    dist[r][c] = dist[i][j] + 1
                    queue.append([r, c])

        # Return
        return dist


if __name__ == '__main__':
    grid = [[0, 1, 0],
            [1, 1, 1],
            [1, 1, 1]]

    sol = Solution()
    print(sol.updateMatrix(grid))
