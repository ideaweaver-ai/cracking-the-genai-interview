'''
shortest path in grid
shortest path len in grid
'''

from collections import deque


def shortest_path(grid, sr, sc, tr, tc):
    rows = len(grid)
    cols = len(grid[0])

    seen = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque()
    count = 0

    queue.append([sr, sc, count, [(sr, sc)]])
    seen[sr][sc] = True

    while queue:
        sr, sc, count, current_path = queue.popleft()

        if sr == tr and sc == tc:
            return [count, current_path]

        potential_neighbors = {(sr, sc + 1), (sr, sc - 1), (sr + 1, sc), (sr - 1, sc)}
        potential_knight_neighbors = {(sr - 2, sc + 1), (sr - 1, sc + 2), (sr + 1, sc + 2), (sr + 2, sc + 1),
                                      (sr - 2, sc - 1), (sr - 1, sc - 2), (sr + 1, sc - 2), (sr + 2, sc - 1)}
        for r, c in potential_knight_neighbors:
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1 and seen[r][c] is False:
                queue.append([r, c, count + 1, current_path + [(r, c)]])
                seen[r][c] = True
    return None


grid = [[1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1]]

print(shortest_path(grid, 0, 0, 2, 4))

