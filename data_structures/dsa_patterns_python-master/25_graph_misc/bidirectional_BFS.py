'''
Bidirectional BFS
'''

from collections import deque


class Node:
    def __init__(self, val=None, visited=False, neighbors=[]):
        self.val = val
        self.neighbors = neighbors
        self.visited = visited


# returns [bool, # of hops]
def bi_bfs(src: Node, dst: Node) -> [bool, int]:
    if src.val == dst.val:
        return True

    queue_s = deque()
    queue_d = deque()

    queue_s.append(src)
    src.visited = True

    queue_d.append(dst)
    dst.visited = True
    num_of_hops = 0

    while queue_s and queue_d:
        s_node = queue_s.popleft()
        d_node = queue_d.popleft()

        if is_there_same_node(s_node.neighbors, d_node.neighbors):
            return [True, num_of_hops]

        for s in s_node.neighbors:
            if s == dst or s == d_node:
                return [True, num_of_hops]
            if s.visited is False:
                queue_s.append(s)
                s.visited = True

        for d in d_node.neighbors:
            if d == src or d == s_node:
                return [True, num_of_hops]
            if d.visited is False:
                queue_d.append(d)
                d.visited = True

        num_of_hops += 1

    return [False, num_of_hops]


def is_there_same_node(a, b):
    a_set = set(a)
    for x in b:
        if x in a_set:
            return True

    return False


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n5 = Node(5)
n6 = Node(6)
n7 = Node(7)
n8 = Node(8)
n9 = Node(9)
n10 = Node(10)
#       2               7
#     /   \           /   \
#   1      4 -- 5 -- 6     9    10
#     \   /           \   /
#       3               8

n1.neighbors = [n2, n3]
n2.neighbors = [n1, n4]
n3.neighbors = [n1, n4]
n4.neighbors = [n2, n3, n5]
n5.neighbors = [n4, n6]
n6.neighbors = [n5, n7, n8]
n7.neighbors = [n6, n9]
n8.neighbors = [n6, n9]
n9.neighbors = [n7, n8]
n10.neighbors = []

# a simple chain graph
# n1.neighbors = [n2]
# n2.neighbors = [n1, n3]
# n3.neighbors = [n2, n4]
# n4.neighbors = [n3, n5]
# n5.neighbors = [n4, n6]
# n6.neighbors = [n5, n7]
# n7.neighbors = [n6, n8]
# n8.neighbors = [n7]

print(bi_bfs(n1, n7))
