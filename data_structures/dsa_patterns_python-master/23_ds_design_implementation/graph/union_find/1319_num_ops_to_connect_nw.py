from typing import List

class Solution:
    # Union find by rank
    # Count number of edges that create cycle
    # Count number of connected components
    # if extra edges > num connected comps - 1 return num connected comps - 1
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:

        # O(log(n)) - amortized O(1)
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        def union(x, y, extra_edges):
            xset = find(x)
            yset = find(y)

            if xset != yset:
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:
                    parent[yset] = xset
                    rank[xset] += 1
            else:
                extra_edges += 1
            return extra_edges

        # main function
        # can use integer as we know num of nodes
        parent = [i for i in range(n)]
        rank = [0 for i in range(n)]

        # count extra edges
        extra_edges = 0

        # perform union and count extra edges
        for i, j in connections:
            extra_edges = union(i, j, extra_edges)

        # count connected components
        connected_comps = 0
        for index, val in enumerate(parent):
            if val == index:  # root(parent) of connected compponent
                connected_comps += 1

        # Is it possible to connect
        return connected_comps - 1 if extra_edges >= connected_comps - 1 else -1


if __name__ == '__main__':
    n = 6
    connections = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]
    sol = Solution()
    print(sol.makeConnected(n, connections))