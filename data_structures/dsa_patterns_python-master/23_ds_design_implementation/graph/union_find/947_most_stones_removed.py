from typing import List

#
# # Time O(n*log(n)) | Space: O(n)
# class Solution:
#     # union find without rank
#
#     # We want to count connected components (islands) in the graph
#     # In each island we  can collect all the stones but 1
#     # Ans will be num of stones - num of islands
#
#     # Note - an element of stones list is not an edge of the graph
#     def removeStones(self, stones: List[List[int]]) -> int:
#         # The focus is counting connected components(islands)
#
#         # Although row cell, column cell is not an edge if we treat them as one they
#         # will belong to the same connected component
#
#         # Now when we split a stone coordinates as row cell, column cell stones having same row
#         # or cell will belong to the same collected component
#
#         def find(i):
#             if parent[i] != i:  # can use -1 too
#                 parent[i] = find(parent[i])
#             return parent[i]
#
#         def union(x, y):
#             # No need to detect cycle in this case
#
#             parent.setdefault(x, x)
#             parent.setdefault(y, y)
#
#             xset = find(x)
#             yset = find(y)
#
#
#             if xset != yset:
#                 parent[yset] = xset
#
#         # since we dont know vertices beforehand
#         parent = {}
#         # rank = {}
#
#         for x, y in stones:
#
#             # find union - make it part of connected component having stones in same row/col
#             union(x, ~y) # twiddle used - differentiate betweeen row and col e.g.0,0 can use 10000+, just make sure its max num in problem
#
#             # num stones - num connected components
#         return len(stones) - len({find(x) for x, y in stones})


# Time O(n*log(n)) | Space: O(n)
class Solution:
    # union find with rank

    # We want to count connected components (islands) in the graph
    # In each island we  can collect all the stones but 1
    # Ans will be num of stones - num of islands

    # Note - a stone in the stones list is not an edge of the graph
    # How do we comvert it into graph ?
    # A stone with coordinate (x, y) is connected to all stones in row x and col y
    # The vertices in the graph should be row and col (nums)
    # and for stone (x,y) we should connect row x and column y
    # problem ? rows range from 0 to n-1 and cols range from 0 to n-1
    # So we need to identify cols with different vertex nums (either ~y - two's compliment, or 10000+y since range of rows and cols is different)
    def removeStones(self, stones: List[List[int]]) -> int:
        # The focus is counting connected components(islands)

        # Although row cell, column cell is not an edge if we treat them as one they
        # will belong to the same connected component

        # Now when we split a stone coordinates as row cell, column cell stones having same row
        # or cell will belong to the same collected component

        def find(i):
            # set default values for parent (and rank ) if accessing node for first time
            parent.setdefault(i, i)
            rank.setdefault(i, 0)
            if parent[i] != i:  # can use -1 too
                parent[i] = find(parent[i])
            return parent[i]

        def union(x, y):
            # No need to detect cycle in this case

            xset = find(x)
            yset = find(y)

            if xset != yset:
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[xset] < rank[yset]:
                    parent[xset] = yset
                else:
                    # set anybody as parent, increase rank of parent by 1
                    parent[yset] = xset
                    rank[xset] += 1

        # since we dont know vertices beforehand
        parent = {}
        rank = {}

        for x, y in stones:
            # find union - make it part of connected component having stones in same row/col
            # ** imp either use ~y or 10000+y to differentiate row and column vertices
            union(x, ~y)

            # num stones - num connected components
        return len(stones) - len({find(x) for x, y in stones})


if __name__ == '__main__':
    stones = [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]
    sol = Solution()
    print(sol.removeStones(stones))








