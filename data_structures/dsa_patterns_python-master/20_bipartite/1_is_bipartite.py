# Copyright © 2020 way2FAANG
# LeetCode: 785

from typing import List
# algorithm
# start at first node of each connected component with  a color (0)
# use bfs or dfs to iterate through the connected component
# if any if the neighbor has same color as current node, its not bipartite.
# otherwise color the neoghbors with alternate color (1) and continue


# DFS solution
# Time: O(V + E) | Space: O(V + E)
class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        def dfs(node, node_color):
            # mark visited (mark with given color)
            color[node] = node_color

            # call bipartiste on neighbors
            is_component_bipartite = True
            for neighbor in graph[node]:
                if color[neighbor] == node_color:  # neighbor has same color as current node - cannot be bipartiste
                    return False

                # if node is not visited earlier (uncolored)
                if color[neighbor] == -1:
                    is_component_bipartite &= dfs(neighbor, 1 - node_color)

            return is_component_bipartite

        vertices = len(graph)
        # initialize - nodes are not colored
        color = [-1 for _ in range(vertices)]

        # call dfs on every connected component (take care of disconnected graph)
        for vertex in range(vertices):
            if color[vertex] == -1:
                if not dfs(vertex, 0):
                    return False
        return True


from collections import deque

# BFS solution
# Time: O(V + E) | Space: O(V + E)
class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:

        vertices = len(graph)
        # initialize - nodes are not colored
        color = [-1 for _ in range(vertices)]

        # initialize bfs queue
        queue = deque()

        # call dfs on every connected component (take care of disconnected graph)
        for vertex in range(vertices):
            if color[vertex] == -1:
                # start bfs
                queue.append(vertex)
                # mark it visited
                color[vertex] = 0

                while queue:
                    current_node = queue.popleft()
                    for neighbor in graph[current_node]:
                        if color[neighbor] == color[current_node]:
                            return False
                        if color[neighbor] == -1:
                            # mark with alternate color (visited)
                            color[neighbor] = 1 - color[current_node]
                            # append to queue
                            queue.append(neighbor)

        return True

