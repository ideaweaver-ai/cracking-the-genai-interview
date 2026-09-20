# Copyright © 2020 way2FAANG

# LeetCode: 733

from typing import List
# Time: O(r*c) | Space: O(r*c)


# DFS
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:

        def dfs_helper(i, j):
            # Change color equivalent to marking visited
            image[i][j] = newColor

            potential_neighbors = [[i + 1, j],
                                   [i - 1, j],
                                   [i, j + 1],
                                   [i, j - 1]]

            for r, c in potential_neighbors:
                # Validate neighbors
                if 0 <= r < rows and 0 <= c < cols and image[r][c] == start_color:
                    dfs_helper(r, c)

        # Main function
        # Input validation
        if not image or sr < 0 or sc < 0:
            return image

        # Rows and cols
        rows = len(image)
        cols = len(image[0])

        # starting pixel color
        start_color = image[sr][sc]
        # nothing to do if start color and new color are same
        if start_color == newColor:
            return image

        dfs_helper(sr, sc)

        return image


# DFS iterative -using stack
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:

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
    sr = 1
    sc = 1
    newColor = 2
    sol = Solution()
    print(sol.floodFill(image, sr, sc, newColor))
