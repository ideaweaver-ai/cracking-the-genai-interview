# Copyright © 2020 way2FAANG
# LeetCode: 310


from collections import deque


def find_trees(nodes, edges):
    # Input validation
    if nodes < 0 or not edges:
        return []

    if nodes == 1:
        return nodes

    # 1. Init graph
    graph = {i: [] for i in range(nodes)}
    degree = {i: 0 for i in range(nodes)}

    # 2. Build graph
    # Imp we need to build a undirected graph in this case (since any node can be root)
    # so for each edge in edges  - there will be 2 edges
    for edge in edges:
        node1, node2 = edge
        graph[node1].append(node2)
        graph[node2].append(node1)
        degree[node1] += 1
        degree[node2] += 1

    # 3. Add initial leaves to the bfs queue - a node is a leaf if its degree is 1
    leaves = deque()
    for node in degree:
        if degree[node] == 1:
            leaves.append(node)

    # 4. topological sort
    total_nodes = nodes

    # Max there could be 1 or 2 nodes with MHT (try with 3 and 4)
    while total_nodes > 2:
        # Update total_nodes (since leaves will be popped in each iteration of topological sort)
        # Bfs level_size - capture the leaves size here - dont use len(leaves) as it will constantly updated
        leaves_size = len(leaves)

        for _ in range(leaves_size):
            leaf = leaves.popleft()
            for vertex in graph[leaf]:
                degree[vertex] -= 1
                if degree[vertex] == 1:
                    leaves.append(vertex)

        # reduce total number of nodes
        total_nodes -= leaves_size

    return list(leaves)


def main():
    print("Roots of MHTs: " +
          str(find_trees(5, [[0, 1], [1, 2], [1, 3], [2, 4]])))
    print("Roots of MHTs: " +
          str(find_trees(4, [[0, 1], [0, 2], [2, 3]])))
    print("Roots of MHTs: " +
          str(find_trees(4, [[1, 2], [1, 3]])))


main()
