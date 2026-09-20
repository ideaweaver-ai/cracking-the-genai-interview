

# Union Find - Naive version
def find_disjoint_sets(n, edges):
    # O(n)
    def find(i):
        # root of the component (sub-graph) found
        if parent[i] == i:
            return i
        return find(parent[i])

    # O(n)
    def union(x, y):
        # Find parents (set roots) of the two nodes
        xset = find(x)
        yset = find(y)

        # # we can also detect cycle here (parent for x and y are same)
        # if xset == yset:
        #     # cycle detected
        #     return True

        # If the parents are not same then joint he two disjoint sets
        if xset != yset:
            parent[yset] = xset

    # Define parent
    parent = [i for i in range(n)]

    for source, dest in edges:
        union(source, dest)

    # count number of disjoint sets
    num_of_disjoint_sets = 0
    for i in range(n):
        if i == parent[i]:
            # this is root of the component/ sub-graph/ disjoint set
            num_of_disjoint_sets += 1

    return num_of_disjoint_sets


# Union Find - using rank and path compression
def find_disjoint_sets(n, edges):
    # O(log(n))
    # Path compression
    def find(i):
        # root of the component (sub-graph) found
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    # O(log(n))
    # Weighted union by rank
    def union(x, y):
        # Find parents (set roots) of the two nodes
        xset = find(x)
        yset = find(y)

        # # we can also detect cycle here (parent for x and y are same)
        # if xset == yset:
        #     # cycle detected
        #     return True

        # If the parents are not same then joint he two disjoint sets
        if xset != yset:
            if rank[xset] > rank[yset]:
                parent[yset] = xset
            elif rank[xset] < rank[yset]:
                parent[xset] = yset
            else:   # rank[xset] == rank[yset]
                parent[yset] = xset
                rank[xset] += 1

    # Define parent and rank
    parent = [i for i in range(n)]
    rank = [0 for _ in range(n)]

    for source, dest in edges:
        union(source, dest)

    # count number of disjoint sets
    num_of_disjoint_sets = 0
    for i in range(n):
        if i == parent[i]:
            # this is root of the component/ sub-graph/ disjoint set
            num_of_disjoint_sets += 1

    return num_of_disjoint_sets


if __name__ == '__main__':
    n = 9
    edges = [[0, 1], [1, 2], [2, 3], [3, 4], [5, 6], [6, 7], [7, 8]]
    print(find_disjoint_sets(n, edges))
