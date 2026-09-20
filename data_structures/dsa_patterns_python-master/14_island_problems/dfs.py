# Copyright © 2020 way2FAANG

# Basic DFS
# n -> number of vertices. The vertices are numbered from 0 to n-1
# edges -> edges between the vertices

from typing import List


# Time: O(V+E), Space: O(V+E)
def create_adjacency_list(n: int, edges: List[List[int]]):
    graph = {i: [] for i in range(n)}

    for source, dest in edges:
        try:
            graph[source].append(dest)
        except IndexError:
            print('Invalid edge')

    return graph


# Time: O(V+E), Space: O(V+E)
def depth_first_search(n: int, edges: List[List[int]]):
    # helper function defined as inner function so we dont have to pass result and adjacency list every time
    def depth_first_search_helper(node):
        # # base case
        # if visited[node]:
        #     return

        # Process node
        result.append(node)
        visited[node] = True

        # Recursive calls
        for neighbor in adjacency_list[node]:
            if not visited[neighbor]:
                depth_first_search_helper(neighbor)

    # output var
    result = []

    # Create graph
    adjacency_list = create_adjacency_list(n, edges)

    # For graph we need visited for each node - implement either as array or property of graph node
    visited = {i: False for i in range(n)}

    # Start dfs for every connected component
    for i in range(n):
        if not visited[i]:
            depth_first_search_helper(i)

    # Calling the depth first search will update the result
    return result


# DFS iterative using stack
def depth_first_search_iterative(n: int, edges: List[List[int]]):
    # output var
    result = []

    # Create graph
    adjacency_list = create_adjacency_list(n, edges)

    # For graph we need visited for each node - implement either as array or property of graph node
    visited = {i: False for i in range(n)}

    # Define stack for dfs
    stack = []

    # Start dfs for every connected component
    for i in range(n):
        if not visited[i]:
            # Add initial elements and mark them visited
            visited[i] = True
            stack.append(i)

            # DFS for this connected component
            while stack:
                # Get current node and add current node to result
                current_node = stack.pop()
                result.append(current_node)

                # Iterate through neighbors
                for neighbor in adjacency_list[current_node]:
                    # ** Since graph can have cycle, check and add only non visited nodes
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)

    return result


if __name__ == '__main__':
    n = 9
    edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [2, 6], [2, 7], [5, 6], [6, 7], [3, 8]]
    print('Note: DFS and Iterative DFS with stack will give different order')
    print(depth_first_search(n, edges))
    print(depth_first_search_iterative(n, edges))
