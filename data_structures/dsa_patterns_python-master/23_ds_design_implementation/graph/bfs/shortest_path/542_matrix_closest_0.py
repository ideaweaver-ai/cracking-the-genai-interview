from typing import List
from collections import deque


class Solution:
    # Brute force
    # Worst case O( (rows*cols)**2) - for each 1 we need to scan the matrix
    # BFS
    # 1. whenever we find 1 - use bfs to find closest 0. Again we could end up with same TC as brute force
    # 2. for each 0 we update the neighbors distance and put hem in queue - O(r*c)

    #     def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
    #         rows = len(matrix)
    #         columns = len(matrix[0])
    #         # while creating multidimensinal arrays got last dimension to first dimension
    #         dist = [[float('inf') for _ in range(columns)] for _ in range(rows)]

    #         for i in range(rows):
    #             for j in range(columns):
    #                 if matrix[i][j] == 0:
    #                     dist[i][j] = 0
    #                 else:
    #                     for l in range(rows):
    #                         for k in range(columns):
    #                             if matrix[l][k] == 0:
    #                                 current_dist = abs(l-i) + abs(k-j)
    #                                 dist[i][j] = min(dist[i][j], current_dist)
    #         return dist

    # BFS - O(r*c) time | O(r*c) space
    # def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
    #     # Don't need to pass parameters
    #     def get_valid_nieghbors(i, j):
    #         potential_neighbors = [[i, j + 1], [i + 1, j], [i, j - 1], [i - 1, j]]
    #         valid_neighbors = []
    #         for r, c in potential_neighbors:
    #             if 0 <= r < rows and 0 <= c < columns and matrix[r][c] != 0 and not visited[r][c]:
    #                 valid_neighbors.append([r, c])
    #         return valid_neighbors
    #
    #     # get rows and columns
    #     rows = len(matrix)
    #     columns = len(matrix[0])
    #
    #     # Output var
    #     # while creating multidimensinal arrays go last dimension to first dimension
    #     dist = [[float('inf') for _ in range(columns)] for _ in range(rows)]
    #
    #     # Bfs queue
    #     queue = deque()
    #
    #     # visited
    #     visited = [[False for _ in range(columns)] for _ in range(rows)]
    #
    #     # Add elements with zero to the queue and update dist - slightly different
    #     for i in range(rows):
    #         for j in range(columns):
    #             if matrix[i][j] == 0:
    #                 # update result
    #                 dist[i][j] = 0
    #                 # Add to queue
    #                 queue.append([i, j])
    #                 # Mark visited
    #                 visited[i][j] = True
    #     while queue:
    #         i, j = queue.popleft()
    #         for r, c in get_valid_nieghbors(i, j):
    #             # We don't need to worry about dist for a node being updated twice
    #             # if the neighbor is near to a 0 it would have been updated earlier as all 0's were added to the que first
    #             # and since we are updating only in case new dist is less than current distance
    #             dist[r][c] = min(dist[r][c], dist[i][j] + 1)
    #             visited[r][c] = True
    #             queue.append([r, c])
    #
    #     return dist

    # BFS -same complexity without using visited
    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:

        # Get rows and cols
        rows = len(matrix)
        cols = len(matrix[0])

        dist = [[float('inf') for i in range(cols)] for j in range(rows)]

        # initialize distances and queue
        queue = deque()
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    dist[i][j] = 0
                    queue.append([i, j])

        while queue:
            # Get current node
            i, j = queue.popleft()

            # update neighbors if dist is minimum
            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            # Update the distance of neighbors if less than current distance and add them to queue
            for r, c in potential_neighbors:
                if 0 <= r < rows and 0 <= c < cols:
                    if dist[r][c] > dist[i][j] + 1:
                        dist[r][c] = dist[i][j] + 1
                        queue.append([r, c])

        # Return
        return dist


if __name__ == '__main__':
    solution = Solution()
    matrix = [[0,0,0], [0,1,0], [1,1,1]]
    print(solution.updateMatrix(matrix))