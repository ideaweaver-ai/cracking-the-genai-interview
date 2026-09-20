from collections import deque


def create_adjacency_list(n, edges):
    adjacency_list = [[] for _ in range(n)]
    for source, dest in edges:
        try:
            adjacency_list[source].append(dest)
        except IndexError:
            print('Invalid edge')
    return adjacency_list


def breadth_first_search(n, edges):

    result = []

    visited = [False for _ in range(n)]

    # get adjacencny list
    adjacency_list = create_adjacency_list(n, edges)

    # Create bfs queue
    queue = deque()

    # Add initial values to bfs queue and mark them visited
    queue.append(0)
    visited[0] = True

    # bfs iterate through queue
    while queue:
        current_node = queue.popleft()
        result.append(current_node)

        for neighbor in adjacency_list[current_node]:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True

    return result


if __name__ == '__main__':
    n = 9
    edges = [[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [2, 6], [2, 7], [5, 6], [6, 7], [3, 8]]
    print(breadth_first_search(n, edges))