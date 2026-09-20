from typing import List

from collections import deque

# BFS solution - same time and space complexity
# class Solution:
#     # This problem can be solved by BFS and DFS solutions
#     # BFS solution
#     def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
#
#         # number of rooms
#         n = len(rooms)
#
#         # visited
#         visited = [False] * n
#
#         # BFS queue and add 0 (since only 0 is open at the start)
#         queue = deque()
#         queue.append(0)
#
#         while queue:
#             # deque current node
#             current_room = queue.popleft()
#             # mark visited
#             visited[current_room] = True
#
#             for neighbor in rooms[current_room]:
#                 if not visited[neighbor]:
#                     queue.append(neighbor)
#
#         return sum(visited) == n

# Better dfs solution
class Solution:
    # This problem can be solved by BFS and DFS solutions
    # DFS solution
    # Time: O(n+k) - number of rooms + num of total keys (fetched from each room - room[i])
    # Space: O(n) - visited and stack space
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        def dfs_helper(current_room):

            # we are calling dfs only on unvisited rooms
            visited[current_room] = True
            for neighbor in rooms[current_room]:
                if not visited[neighbor]:
                    dfs_helper(neighbor)

        # Input validation
        if not rooms:
            return True

        # main function
        n = len(rooms)
        visited = [False] * n

        # call dfs on room 0 - since only it is unlocked at start
        dfs_helper(0)
        return sum(visited) == n


if __name__ == '__main__':
    rooms = [[1], [2], [3], []]
    sol = Solution()
    print(sol.canVisitAllRooms(rooms))

    rooms = [[1, 3], [3, 0, 1], [2], [0]]
    sol = Solution()
    print(sol.canVisitAllRooms(rooms))
