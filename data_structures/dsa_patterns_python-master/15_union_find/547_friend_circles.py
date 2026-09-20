# Copyright © 2020 way2FAANG
# LeetCode: 547

from typing import List


class Solution:
    # DFS solution
    # view M as an adjacency list
    # Time: O(n**2) time | O(n) space - visited, O(n) space - stack
    # def findCircleNum(self, M: List[List[int]]) -> int:
    #     def dfs(i):
    #         for j in range(vertices):
    #             if M[i][j] == 1 and not visited[j]:
    #                 # Mark visited
    #                 visited[j] = True  # this will cover the case of marking itself as visited
    #                 dfs(j)
    #
    #     # Input validation
    #     if not M:
    #         return 0
    #
    #     # Output var
    #     friend_circles = 0
    #
    #     # Get number of vertices
    #     vertices = len(M)
    #
    #     # visited flag
    #     visited = [False] * vertices
    #
    #     # Iterate through each vertex and perform dfs
    #     # Whenever we performa a new dfs increase count
    #     for i in range(vertices):
    #         if not visited[i]:
    #             friend_circles += 1
    #             dfs(i)
    #
    #     return friend_circles

    # dfs solution
    # Without using visible flag
    # Time: O(n**2) | Space: O(n) for recursion
    # class Solution:
    #     def findCircleNum(self, M: List[List[int]]) -> int:
    #         def dfs(i):
    #             for neighbor in range(n):
    #                 if neighbor != i and M[i][neighbor] == 1 and M[neighbor][neighbor] == 1:
    #                     # mark visited
    #                     M[neighbor][neighbor] = 0
    #                     dfs(neighbor)
    #
    #                     # O/p variable
    #
    #         friend_circles = 0
    #
    #         # Get vertices
    #         n = len(M)
    #
    #         # we are not using visited flag, we will change the input matrix to mark visited
    #
    #         # visit each unvisited vertex and do dfs to cover that friend circle
    #         for i in range(n):
    #             # mark visited - we can mark visted in the dfs helper function
    #             # but to maintain consistency of pattern we mark visited and then perform dfs
    #             if M[i][i] == 1:  # this vertex is still not visited
    #                 # increase count of friend circles
    #                 friend_circles += 1
    #                 # mark visited
    #                 M[i][i] = 0
    #                 # DFS
    #                 dfs(i)
    #
    #         return friend_circles

    # # BFS solution
    # # view M as an adjacency list
    # # Time: O(n**2) time | O(n) space - visited, O(n) space - stack
    # def findCircleNum(self, M: List[List[int]]) -> int:
    #     # Input validation
    #     if not M:
    #         return 0
    #
    #     # Output var
    #     friend_circles = 0
    #
    #     # Get number of vertices
    #     vertices = len(M)
    #
    #     # visited flag
    #     visited = [False] * vertices
    #
    #     # BFS queue
    #     queue = deque()
    #
    #     # Iterate through each vertex and perform bfs
    #     # Whenever we performa a new bfs increase count
    #     for vertex in range(vertices):
    #         if not visited[vertex]:
    #             friend_circles += 1
    #             queue.append(vertex)
    #             while queue:
    #                 i = queue.popleft()
    #                 visited[i] = True
    #                 for j in range(vertices):
    #                     if M[i][j] == 1 and not visited[j]:
    #                         queue.append(j)
    #
    #     return friend_circles

    # Union find by rank and path compression
    # view M as an adjacency list
    # Time: O(n**2 * log(n))
    def findCircleNum(self, M: List[List[int]]) -> int:
        # Time: O(log(n))
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        # Time: O(log(n))
        def union(x, y):
            # find parents
            xset = find(x)
            yset = find(y)

            # belong to different friend circles (disjoint sets)
            # since there is an edge we need to combine them into 1 circle
            if xset != yset:
                # Higher ranked node becomes the parent of the combined friend circle
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:
                    parent[yset] = xset
                    rank[xset] += 1

        # o/p var
        friend_circles = 0

        # Get number of vertices
        n = len(M)

        # Define parent
        parent = [i for i in range(n)]

        # Define rank
        rank = [0 for _ in range(n)]

        # perform union based on edges
        for i in range(n):
            for j in range(n):
                if j != i and M[i][j] == 1:
                    union(i, j)

        # calculate the number of friend circles (disjoint sets)
        for i in range(n):
            if parent[i] == i:
                friend_circles += 1

        return friend_circles


if __name__ == '__main__':
    M = [[1, 1, 0],
         [1, 1, 0],
         [0, 0, 1]]

    sol = Solution()
    print(sol.findCircleNum((M)))
