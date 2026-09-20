
from typing import List
from collections import deque


def create_adjacency_list(n: int, edges: List[List[int]]):
    adjacency_list = [[] for _ in range(n)]

    for source, dest in edges:
        try:
            adjacency_list[source].append(dest)
        except IndexError:
            print('Invalid edge')

    return adjacency_list


def breadth_first_search(n: int, edges: List[List[int]]):
    # Assuming BFS starts from 0

    # output var
    result = []

    # Create graph
    adjacency_list = create_adjacency_list(n, edges)

    # For graph we need visited for each node - implement either as array or property of graph node
    visited = [False] * n

    # Define BFS queue
    queue = deque()
    # Add initial values and mark them visited
    # better to mark visited when node is enqueued to queue
    # we can do it when we deque but it will give error for iterative dfs using stack
    queue.append(0)
    visited[0] = True

    # BFS
    while queue:
        # We don't need level wise seperation
        current_node = queue.popleft()

        # Add current node to result
        result.append(current_node)
        # Iterate through neighbors
        for neighbor in adjacency_list[current_node]:
            # ** Since graph can have cycle, check and add only non visited nodes
            if not visited[neighbor]:
                # add to queue
                queue.append(neighbor)
                # mark visited when enquing - better practice
                visited[neighbor] = True

    return result


if __name__ == '__main__':
    n = 9
    edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [2, 6], [2, 7], [5, 6], [6, 7], [3, 8]]
    print(breadth_first_search(n, edges))
