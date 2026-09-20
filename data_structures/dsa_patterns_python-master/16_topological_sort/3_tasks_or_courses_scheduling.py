# Copyright © 2020 way2FAANG
# LeetCode: 210

from collections import deque


# Time - O(V+E) time, since every vertex and edge to be visited once | space - O(V+E) for adjacency list
def find_order(tasks, prerequisites):
    # Output var
    sorted_order = []

    # Input validation
    if tasks <= 0:
        return sorted_order

    # 1. Initialize graph - O(V)
    graph = {i: [] for i in range(tasks)}  # O(V + E)
    in_degree = {i: 0 for i in range(tasks)}  # O(V) space

    # 2. Build the graph - O(E)
    for parent, child in prerequisites:
        graph[parent].append(child)
        in_degree[child] += 1

    # 3.Add initial sources to queue
    # O(V+E)
    sources = deque()  # O(V) space
    for vertex in in_degree:
        if in_degree[vertex] == 0:
            sources.append(vertex)

    # 4. BFS through queue. Each source can be added to result?
    # Now since parent task completed it can be removed as dependency for child - reduce in_degree by 1 for each of its children
    while sources:
        vertex = sources.popleft()
        sorted_order.append(vertex)
        for child in graph[vertex]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                sources.append(child)

    return sorted_order if len(sorted_order) == tasks else []


def main():
    print("Is scheduling possible: " + str(find_order(3, [[0, 1], [1, 2]])))
    print("Is scheduling possible: " +
          str(find_order(3, [[0, 1], [1, 2], [2, 0]])))
    print("Is scheduling possible: " +
          str(find_order(6, [[2, 5], [0, 5], [0, 4], [1, 4], [3, 2], [1, 3]])))


main()
