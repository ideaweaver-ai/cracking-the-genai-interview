from typing import List


def create_adjacency_list(n: int, edges: List[List[int]]):
    adjacency_list = [[] for _ in range(n)]

    for source, dest in edges:
        try:
            adjacency_list[source].append(dest)
        except IndexError:
            print('Invalid edge')

    return adjacency_list


def depth_first_search(n: int, edges: List[List[int]]):

    # helper function defined as inner function so we dont have to pass result and adjacency list every time
    def depth_first_search_helper(node):
        # base case
        if visited[node]:
            return
        # Process node
        result.append(node)
        visited[node] = True
        # Recursive calls
        for neighbor in adjacency_list[node]:
            depth_first_search_helper(neighbor)

    # output var
    result = []

    # Create graph
    adjacency_list = create_adjacency_list(n, edges)

    # For graph we need visited for each node - implement either as array or property of graph node
    visited = [False] * n

    # Define BFS and add source
    depth_first_search_helper(0)

    # Calling the depth first search will update the result
    return result



if __name__ == '__main__':
    n = 9
    edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [2, 6], [2, 7], [5, 6], [6, 7], [3, 8]]
    print(depth_first_search(n, edges))
