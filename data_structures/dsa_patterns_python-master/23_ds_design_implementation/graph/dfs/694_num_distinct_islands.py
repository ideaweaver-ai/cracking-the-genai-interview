from typing import List


class Solution:
    def numDistinctIslands(self, grid: List[List[int]]) -> int:

        def dfs_helper(i, j, dirn, shape):
            # Check right at start so you don't have to check it in for loop
            if 0 <= i < rows and 0 <= j < cols and grid[i][j] == 1 and (i, j) not in visited:

                # mark visited
                visited.add((i, j))
                # append shape
                shape.append(dirn)

                potential_neighbors = [[i, j + 1, 1], [i, j - 1, 2],
                                       [i + 1, j, 3], [i - 1, j, 4]]

                # Check which neighbors are valid and call dfs on them
                for r, c, dirn in potential_neighbors:
                    dfs_helper(r, c, dirn, shape)

                # dfs explores 1 path, then second path and so on from the start node
                # shape of island is all these paths appended in serial order (one by one)
                # if we don't add 0 at end, then 1 shape can be just 1 path or two paths
                # try example - write a shape (without 0 at end) - you could write just
                # one path with this or 2 paths or 3 ...
                # when we 0 at end of shape we knwhen a path end
                shape.append(0)  # very important, otherwise some test cases fail

        ## Main function
        # validate inputs
        if not grid:
            return 0

        # get rows and cols
        rows = len(grid)
        cols = len(grid[0])

        # visited handled by making cell 0, don;'t need visited matrix
        # if told dont modify input use visited array
        visited = set()

        # result - to compare island shapes (set) and get count
        # need to maintain shape of island to see if it is unique
        result = set()

        # go element wise in grid and perform dfs at every 1
        for i in range(rows):
            for j in range(cols):
                # check is happening in dfs and dfs will be performed only wehn cell is 1
                shape = []
                # start dir ->0. This 0 indicates start of island
                # for each individual path we need to add 0 to shape in dfs
                dfs_helper(i, j, 0, shape)
                if shape:
                    result.add(tuple(shape))  # list is immutable, hence cannot be addaed to set. so convert tot tuple

        return len(result)


if __name__ == '__main__':
    grid = [[1, 1, 0, 1, 1],
             [1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1],
             [1, 1, 0, 1, 1]]
    sol = Solution()

    print(sol.numDistinctIslands(grid))
