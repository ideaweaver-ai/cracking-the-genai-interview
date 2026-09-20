from collections import deque
from typing import List


class Solution:

    def orangesRotting(self, grid: List[List[int]]) -> int:
        def getValidNeighbors(i, j):
            potential_neighbors = [[i, j + 1], [i + 1, j], [i, j - 1], [i - 1, j]]
            valid_neighbors = []
            for r, c in potential_neighbors:
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                    valid_neighbors.append([r, c])
            return valid_neighbors

        rows = len(grid)
        cols = len(grid[0])

        # Output vars
        count_fresh = 0
        count_mins = 0

        # Don't need visited as 0, 1 and 2 states can be used to reproduce that logic
        que = deque()

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:
                    que.append([i, j])
                elif grid[i][j] == 1:
                    count_fresh += 1

        # if already rotten - need to handle it here because in case where we have rotten
        # oranges at the start, the ciunt of minutes hsould be reduced by 1
        if count_fresh == 0:
            return count_mins

        while que:
            count_mins += 1
            level_size = len(que)
            for _ in range(level_size):
                i, j = que.popleft()
                for r, c in getValidNeighbors(i, j):
                    grid[r][c] = 2  # mark it rotten
                    count_fresh -= 1
                    que.append([r, c])

        if count_fresh == 0:
            return count_mins - 1  # -1 because last iteration og que will be when a rotten ode is popped and nothing added. So we don't need to count that minute

        return -1


if __name__ == '__main__':
    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    solution = Solution()
    print(solution.orangesRotting(grid))
