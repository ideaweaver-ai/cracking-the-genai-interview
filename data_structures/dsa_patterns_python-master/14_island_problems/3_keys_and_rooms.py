# Copyright © 2020 way2FAANG

# LeetCode: 841

from typing import List
from collections import deque


# All solutions:
# Time: O(n) | Space: O(n) - n is number of rooms


# DFS solution
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        def dfs_helper(current_room):

            # mark visited
            visited[current_room] = True

            # we are calling dfs only on unvisited rooms
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


# Dfs better solution
class Solution:
    def __init__(self):
        # need to define it here
        # since immutable var, it will give 'referenced before assignment' error in nested function
        # as immutable vars are not passed by reference
        self.count = 0

    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:

        def dfsHelper(current_room):
            # Since we are marking a room visited and calling dfs only on valid rooms
            # no need for other base cases

            # Mark this room visited
            visited[current_room] = True

            # Increase count of rooms visited
            self.count += 1

            # Get the keys to other rooms from this room
            for neighbor in rooms[current_room]:
                # if the room is not visited perform dfs (open and get keys) on it
                if neighbor < n and not visited[neighbor]:
                    dfsHelper(neighbor)

        # Get number of rooms
        n = len(rooms)

        # visited flag and number of rooms visited
        visited = [False] * n

        dfsHelper(0)

        return self.count == n


# DFS iterative - using stack
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:

        # number of rooms
        n = len(rooms)

        # visited
        visited = [False] * n

        # DFS stack
        stack = []
        # need to mark visited when adding to queue
        stack.append(0)
        visited[0] = True

        while stack:
            # pop current node
            current_room = stack.pop()

            for neighbor in rooms[current_room]:
                if not visited[neighbor]:
                    stack.append(neighbor)
                    # better to mark visited when adding - wont affect bfs queue but will be crucial in dfs stack
                    visited[neighbor] = True

        return sum(visited) == n


# BFS solution
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:

        # number of rooms
        n = len(rooms)

        # visited
        visited = [False] * n

        # BFS queue and add 0 (since only 0 is open at the start)
        queue = deque()
        queue.append(0)
        # better to mark visited when adding - wont affect bfs queu but will be crucial in dfs tack
        visited[0] = True

        while queue:
            # deque current node
            current_room = queue.popleft()

            for neighbor in rooms[current_room]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    # better to mark visited when adding - wont affect bfs queu but will be crucial in dfs tack
                    visited[neighbor] = True

        return sum(visited) == n


if __name__ == '__main__':
    rooms = [[1], [2], [3], []]
    sol = Solution()
    print(sol.canVisitAllRooms(rooms))

    rooms = [[1, 3], [3, 0, 1], [2], [0]]
    sol = Solution()
    print(sol.canVisitAllRooms(rooms))
