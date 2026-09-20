# Copyright © 2020 way2FAANG
# LeetCode: 444


from collections import deque


# Time: O(V+E) | Space: O(V+E)
def can_construct(originalSeq, sequences):
    # Output var
    sorted_order = []
    # Validate Inputs
    if not originalSeq or not sequences:
        return True

    # 1. Initialize graph
    graph = {vertex: [] for vertex in originalSeq}
    in_degree = {vertex: 0 for vertex in originalSeq}

    # 2. Build graph
    for sequence in sequences:
        for i in range(len(sequence) - 1):
            parent, child = sequence[i], sequence[i + 1]
            # vertex not par tof original sequence
            if parent not in graph or child not in graph:
                return False

            # normal way to build graph
            graph[parent].append(child)
            in_degree[child] += 1
            # In case multiple edges created to a node like 1-> 5 and 1->5,
            # topological sort will take care

    # 3.Add initial sources
    sources = deque()
    for vertex in in_degree:
        if in_degree[vertex] == 0:
            sources.append(vertex)

    # originalSeq index to match
    original_seq_index = 0

    # 4. Topological sort - logic
    while sources:
        # If multiple sources at any point - multiple ordering possible
        if len(sources) > 1:
            return False

        vertex = sources.popleft()
        sorted_order.append(vertex)

        # if the vertex as per our sorting does not match the original seq
        if original_seq_index > len(originalSeq) or originalSeq[original_seq_index] != vertex:
            return False

        original_seq_index += 1

        for child in graph[vertex]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                sources.append(child)

    # 5. Return
    if len(sorted_order) != len(in_degree):  # cycle
        return False

    return True


def main():
    print("Can construct: " +
          str(can_construct([1, 2, 3, 4], [[1, 2], [2, 3], [3, 4]])))
    print("Can construct: " +
          str(can_construct([1, 2, 3, 4], [[1, 2], [2, 3], [2, 4]])))
    print("Can construct: " +
          str(can_construct([3, 1, 4, 2, 5], [[3, 1, 5], [1, 4, 2, 5]])))


main()
