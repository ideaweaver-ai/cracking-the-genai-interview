from typing import List


class Solution:
    # Time O(r*c) time | Space: Length of longest path stack space, worst case O(r*c)
    def floodFill(self, image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:

        def dfsHelper(i, j):
            # New color - this will also mark it visited
            image[i][j] = newColor

            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            for r, c in potential_neighbors:
                # dfs should be called only on valid neighbors
                if 0 <= r < rows and 0 <= c < cols and image[r][c] == source_color:
                    dfsHelper(r, c)

        # Input validation
        if not image:
            return image

        # Get rows and cols
        rows = len(image)
        cols = len(image[0])

        # Get the color of source cell
        source_color = image[sr][sc]

        if source_color == newColor:
            # No need to do anything
            return image

        # Start from source cell and perform dfs to color connected cells having source color
        dfsHelper(sr, sc)

        return image


# DFS since from the start we need to cover all connected cells

# DFS iterative -using stack
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:

        def dfs_helper(i, j):
            # Change color and mark visited
            image[i][j] = newColor
            visited[i][j] = True

            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            for r, c in potential_neighbors:
                # Validate neighbors
                if 0 <= r < rows and 0 <= c < cols and image[r][c] == start_color and not visited[r][c]:
                    dfs_helper(r, c)

        # Input validation
        if not image:
            return image

        # Rows and cols
        rows = len(image)
        cols = len(image[0])

        # Need visited flag - case where start color is same as new color
        visited = [[False for _ in range(cols)] for _ in range(rows)]

        # starting pixel color
        start_color = image[sr][sc]

        # if start color is same as new color return - e;se time limit will exceed
        if start_color == newColor:
            return image

        # DFS stack
        stack = []
        stack.append([sr, sc])
        # mark visited
        image[sr][sc] = newColor

        # dfs - iterative using stack
        while stack:
            # pop current node
            i, j = stack.pop()

            # potential neighbors
            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            for r, c in potential_neighbors:
                # validate neighbors
                if 0 <= r < rows and 0 <= c < cols and image[r][c] == start_color:
                    stack.append([r, c])
                    # mark visited
                    image[r][c] = newColor

        return image


if __name__ == '__main__':
    image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    sr, sc, newColor = 1, 1,  2
    sol = Solution()
    print(sol.floodFill(image, sr, sc, newColor))
