import math


def shortest_weighted_path(grid):
    if len(grid) == 0:
        return None
    memo = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    return helper(grid, 0, 0, memo)


def helper(grid, i, j, memo):
    rows = len(grid)
    cols = len(grid[0])

    if i == rows - 1 and j == cols - 1:
        return grid[i][j]

    if memo[i][j] != -1:
        return memo[i][j]

    neighbors = []
    if i + 1 < rows:
        neighbors.append((i + 1, j))
    if j + 1 < cols:
        neighbors.append((i, j + 1))

    shortest_path_length = math.inf
    for r, c in neighbors:
        shortest_path_length = min(shortest_path_length, helper(grid, r, c, memo))

    memo[i][j] = grid[i][j] + shortest_path_length
    return memo[i][j]


g = [[0, 2, 3, 2, 4, 5],
     [6, 1, 1, 1, 20, 7],
     [1, 0, 3, 3, 2, 8],
     [1, 1, 4, 3, 2, 0]]

print(shortest_weighted_path(g))
