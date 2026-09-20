from typing import List

def create_adjacency_list(n: int, edges: List[List[int]]) -> List:
    adjacency_list = [[] for _ in range(n)]

    for source, dest in edges:
        try:
            adjacency_list[source].append(dest)
        except IndexError:
            print('Invalid edge')

    return adjacency_list



def depth_first_search(n, edges: List[List[int]]) -> List:

    def dfs(node):
        # # Mark visited
        # visited[node] = True

        # Append to result
        result.append(node)

        for neighbor in adjacency_list[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                dfs(neighbor)

    # output var
    result = []

    # build the graph (adjacency list)
    adjacency_list = create_adjacency_list(n, edges)

    # define visited flag to prevent cycle
    visited = [False for _ in range(n)]

    # call dfs
    visited[0] = True
    dfs(0)

    return result




if __name__ == '__main__':
    n = 9
    edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [2, 6], [2, 7], [5, 6], [6, 7], [3, 8]]
    print(depth_first_search(n, edges))
