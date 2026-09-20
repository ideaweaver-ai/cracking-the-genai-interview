# Copyright © 2020 way2FAANG

# LeetCode: 286

from collections import deque
from typing import List


class Solution:
    # Time: O(r*c) | Space: O(r*c) additional space for queue
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        # Input validation
        if not rooms:
            return rooms

        # Get rows and cols
        rows = len(rooms)
        cols = len(rooms[0])

        # Initialize bfs queue
        # As 0's (gates) determine the dist from gates, add 0's to the queue
        queue = deque()
        for i in range(rows):
            for j in range(cols):
                if rooms[i][j] == 0:
                    queue.append([i, j])

        # bfs
        while queue:
            # current node
            i, j = queue.popleft()

            neighbors = [[i + 1, j],
                         [i - 1, j],
                         [i, j + 1],
                         [i, j - 1]]

            for r, c in neighbors:
                # check valid neighbors
                # since we add to bfs queue only after checking validity, we don't need visited
                if 0 <= r < rows and 0 <= c < cols and rooms[r][c] > 0 and rooms[i][j] + 1 < rooms[r][c]:
                    rooms[r][c] = rooms[i][j] + 1
                    queue.append([r, c])

        return rooms


if __name__ == '__main__':
    INF = 2147483647

    grid = [[INF, -1, 0, INF],
            [INF, INF, INF, -1],
            [INF, -1, INF, -1],
            [0, -1, INF, INF]]

    sol = Solution()
    print(sol.wallsAndGates(grid))
