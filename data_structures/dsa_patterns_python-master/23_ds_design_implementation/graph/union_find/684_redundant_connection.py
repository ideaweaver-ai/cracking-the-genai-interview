from typing import List


class Solution:
    # Disjoint set - union rank
    # Whenever we find an edge whose addition makes a cycle, make it the ans
    # Don't stop keep on going until the end of the graph
    # Time: O(log(V)*E)
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:

        # Disjoint sets
        # O(log(V))
        def find(i):
            # set default values for parent (and rank ) if accessing node for first time
            parent.setdefault(i, i)
            rank.setdefault(i, 0)

            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        # O(log(V))
        def union(x, y):
            """Returns True if union of x and y causes a cycle"""
            xset = find(x)
            yset = find(y)

            # return True if cycle found (this will be the redundant edge)
            if xset != yset:
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:
                    parent[yset] = xset
                    rank[xset] += 1
            else:
                return True

            return False

        # Define parent and rank
        # Since num of vertices are not given, define parent and rank as dictionaries
        # In union and find we will use setdefault to set default values
        parent = {}
        rank = {}

        # Output var
        edge_to_remove = [None, None]

        # Iterate through the graph and find the latest edge whose addition creates a cycle
        for i, j in edges:
            if union(i, j):
                edge_to_remove = [i, j]

        return edge_to_remove


if __name__ == '__main__':
    edges = [[1, 2], [1, 3], [2, 3]]
    sol = Solution()
    print(sol.findRedundantConnection(edges))