# Copyright © 2020 way2FAANG

from collections import deque


# Time - O(V+E) time, since every vertex and edge to be visited once | space - O(V+E) for adjacency list
def topological_sort(vertices, edges):
    # Output var
    sorted_order = []

    # Validate inputs
    if vertices <= 0:
        return sorted_order

    # 1. Initialize the graph
    # O(V)
    in_degree = {i: 0 for i in range(vertices)}  # count of incoming edges
    graph = {i: [] for i in range(vertices)}  # adjacency list graph

    # 2. Build the graph
    # O(E)
    for edge in edges:
        parent, child = edge[0], edge[1]
        graph[parent].append(child)  # put the child into it's parent's list
        in_degree[child] += 1  # increment child's inDegree

    # 3. Fill bfs queue with initial sources - all vertices with 0 in-degrees
    # O(V + E)
    sources = deque()
    for key in in_degree:
        if in_degree[key] == 0:
            sources.append(key)

    # 4. Each source can be added to result. Why? since its inDegree is 0 means there are no dependencies
    # Since parent task completed, its dependency can be removed for child - subtract 1 from each of its children's in-degrees
    # if a child's in-degree becomes zero, add it to the sources queue
    while sources:
        vertex = sources.popleft()
        sorted_order.append(vertex)
        for child in graph[vertex]:  # get the node's children to decrement their in-degrees
            in_degree[child] -= 1
            if in_degree[child] == 0:
                sources.append(child)

    # 5. Return: topological sort is not possible as the graph has a cycle
    if len(sorted_order) != vertices:
        return []

    return sorted_order


def main():
    print("Topological sort: " +
          str(topological_sort(4, [[3, 2], [3, 0], [2, 0], [2, 1]])))
    print("Topological sort: " +
          str(topological_sort(5, [[4, 2], [4, 3], [2, 0], [2, 1], [3, 1]])))
    print("Topological sort: " +
          str(topological_sort(7, [[6, 4], [6, 2], [5, 3], [5, 4], [3, 0], [3, 1], [3, 2], [4, 1]])))


main()
