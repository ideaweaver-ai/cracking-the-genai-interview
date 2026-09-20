# Copyright © 2020 way2FAANG
# LeetCode: 207

from collections import deque


# Time - O(V+E) time, since every vertex and edge to be visited once | space - O(V+E) for adjacency list
def is_scheduling_possible(tasks, prerequisites):
    # Output var
    sorted_order = []

    # Input validation
    if tasks <= 0:
        return True

    # 1. Initialize graph
    adjacency_list = {i: [] for i in range(tasks)}
    in_degree = [0 for _ in range(tasks)]

    # 2. Build the graph
    for parent, child in prerequisites:
        adjacency_list[parent].append(child)
        in_degree[child] += 1

    # 3.Add initial sources to queue
    sources = deque()
    for vertex in range(tasks):
        if in_degree[vertex] == 0:
            sources.append(vertex)

    # 4. BFS through queue. Each source can be added to result?
    # Now since parent task completed it can be removed as dependency for child - reduce in_degree by 1 for each of its children
    while sources:
        current_vertex = sources.popleft()
        sorted_order.append(current_vertex)
        for child in adjacency_list[current_vertex]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                sources.append(child)

    return len(sorted_order) == tasks


def main():
    print("Is scheduling possible: " +
          str(is_scheduling_possible(3, [[0, 1], [1, 2]])))
    print("Is scheduling possible: " +
          str(is_scheduling_possible(3, [[0, 1], [1, 2], [2, 0]])))
    print("Is scheduling possible: " +
          str(is_scheduling_possible(6, [[0, 4], [1, 4], [3, 2], [1, 3]])))


main()
