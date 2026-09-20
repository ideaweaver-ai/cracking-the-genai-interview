from typing import List


# # DFS solution
# # Time: O(V+E) | Space: O(V+E)
# class Solution:
#     def countComponents(self, n: int, edges: List[List[int]]) -> int:
#         def dfs(i):
#             for neighbor in adjacency_list[i]:
#                 # ** imp check if neighbor is not already visited
#                 if not visited[neighbor]:
#                     visited[neighbor] = True
#                     dfs(neighbor)
#
#         def create_adjacency_list():
#             """Create adjacency list to iterate for dfs"""
#             adjacency_list = [[] for _ in range(n)]
#             for source, dest in edges:
#                 # ** imp - this is an undorected graph
#                 adjacency_list[dest].append(source)
#                 adjacency_list[source].append(dest)
#             return adjacency_list
#
#         # visited flag - else we will get infinite depth in recursion
#         visited = [False for _ in range(n)]
#
#         # create adjacency list
#         adjacency_list = create_adjacency_list()
#
#         connected_components = 0
#
#         for i in range(n):
#             if not visited[i]:
#                 # we got a connected component
#                 connected_components += 1
#                 # cover all elements of this connected component using dfs
#                 # mark the node visited and call dfs
#                 visited[i] = True
#                 dfs(i)
#         return connected_components


# Using union find by rank and path compression
# Time: O(V + E*log(V)) | Space: O(V)
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        # Time: O(log(n))
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        # Time: O(log(n))
        def union(x, y):
            xset = find(x)
            yset = find(y)

            if xset != yset:
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:  # rank[xset] == rank[yset]
                    parent[yset] = xset
                    rank[xset] += 1

        # O/p var
        num_connected_comps = 0

        # Define parent
        # Each node forms a disjoint set and is the too of that set
        parent = [i for i in range(n)]

        # Define rank
        rank = [0 for _ in range(n)]

        # Perform union find by iterating over edges
        for source, dest in edges:
            union(source, dest)

        # Count number of connected components (sub-graphs/ disjoint sets)
        for i in range(n):
            if parent[i] == i:
                num_connected_comps += 1

        return num_connected_comps


if __name__ == '__main__':
    n = 5
    edges = [[0, 1], [1, 2], [3, 4]]
    sol = Solution()
    print(sol.countComponents((n, edges)))
