# Copyright © 2020 way2FAANG


from collections import deque


# Time: O(V!*(V+E)) | Space: O(V!(V+E))
def print_orders(tasks, prerequisites):
    # Inner function to prevent passing of all parameters
    def print_orders_helper(sources, sorted_order):
        for current_source in sources:
            # Add current source to result as its dependencies have been satisfied
            sorted_order.append(current_source)
            sources_for_next_call = deque(sources)  # create copy
            # cant remove current vertex from original sources as we want it in the sources list wehn we iterate through other vertices
            sources_for_next_call.remove(current_source)

            # Remove dependencies of the current vertex's children
            # and add them to sources if in_degree becomes 0
            for child in graph[current_source]:
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    sources_for_next_call.append(child)

            # Recursive call to print all combinations of the remaining sources
            print_orders_helper(sources_for_next_call, sorted_order)

            # Backtrack
            sorted_order.remove(current_source)
            for child in graph[current_source]:
                in_degree[child] += 1

        # if sorted_order doesn't contain all tasks, either we've a cyclic dependency between tasks, or
        # we have not processed all the tasks in this recursive call
        if len(sorted_order) == tasks:
            print(sorted_order)

    # Validate inputs
    if tasks <= 0 or not prerequisites:
        return []

    # 1. Initialize graph
    graph = {i: [] for i in range(tasks)}
    in_degree = {i: 0 for i in range(tasks)}

    # 2. Build graph
    for parent, child_ in prerequisites:
        graph[parent].append(child_)
        in_degree[child_] += 1

    # 3. Add initial sources
    sources = deque()
    for current_vertex in range(tasks):
        if in_degree[current_vertex] == 0:
            sources.append(current_vertex)

    # 4. Combination of BFS and DFS to print all paths
    print_orders_helper(sources, [])


def main():
    print("Task Orders: ")
    print_orders(3, [[0, 1], [1, 2]])

    print("Task Orders: ")
    print_orders(4, [[3, 2], [3, 0], [2, 0], [2, 1]])

    print("Task Orders: ")
    print_orders(6, [[2, 5], [0, 5], [0, 4], [1, 4], [3, 2], [1, 3]])


main()
