# Copyright © 2020 way2FAANG
# LeetCode: 269


from collections import deque


# Time - O(V+E) time, since every vertex and edge to be visited once | space - O(V+E) for adjacency list
# V - num of chars, Edges is the num of rules, at max 1 pair of word can give 1 rule. So E is the num of words
def find_order(words):
    # Output var
    sorted_order = []

    # Input validation
    if not words:
        return sorted_order

    # 1. Initialize graph
    graph = {}
    in_degree = {}
    # for word in words:
    #     for c in word:
    #         graph[c] = []
    #         in_degree[c] = 0

    # 2. Build the graph
    # Only this step is different
    for i in range(len(words) - 1):
        # Compare two neighboring words to find graph edges
        w1, w2 = words[i], words[i + 1]
        for j in range(min(len(w1), len(w2))):
            parent, child = w1[j], w2[j]

            if parent != child:
                # Use set default to prevent going through the graph twice (see initialize graph code commented)
                # Use it here instead of if => even if a char does not have relationship but is used in word,
                # it will be a vertex in graph.
                # in this case that does not matter but if asked to return empty string when ordering is not possible
                # it will be useful

                # We cannot use defaultdict ??
                # we will do graph.[parent].append(child), in_degree[child] += 1
                # but we will not add child in graph and parent in in_degree
                # if we do graph[child] = [], in_degree[parent] = 0, it is incorrect
                # because child can be parent of some other node and vice versa
                graph.setdefault(parent, [])
                graph.setdefault(child, [])
                in_degree.setdefault(parent, 0)
                in_degree.setdefault(child, 0)
                graph[parent].append(child)
                in_degree[child] += 1
                # ** imp - Only the first letter that is different will give the  dependency (edge)
                break

    # 3. Add initial sources - vertices where in_degree is 0
    sources = deque()
    for vertex in in_degree:
        if in_degree[vertex] == 0:
            sources.append(vertex)

    # 4 Topological sort
    while sources:
        vertex = sources.popleft()
        sorted_order.append(vertex)

        # Dependency related to current vertex fulfilled - hence we can reduce in degree of children by 1
        # Check if any of them becomes a source
        for child in graph[vertex]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                sources.append(child)

    # 5. Return
    return ''.join(sorted_order) if len(sorted_order) == len(graph) else ""  # cycle


def main():
    print("Character order: " + find_order(["ba", "bc", "ac", "cab"]))
    print("Character order: " + find_order(["cab", "aaa", "aab"]))
    print("Character order: " + find_order(["ywx", "wz", "xww", "xz", "zyy", "zwz"]))


main()
