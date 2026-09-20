# Copyright © 2020 way2FAANG
# LeetCode: 1319
from typing import List

class Solution:
    # Algo:
    # At start of union find, num of connected components = n
    # we want to go on until num of connected componenst left are 1
    # That's the log time we should return
    # Imp - we need to sort the logs at start ? see later

    # Time: N*log(N) + E*log(E) | Space: O(N) + O(E) (for sorting)
    def earliestAcq(self, logs: List[List[int]], N: int) -> int:
        # Time: O(log(N)) | Space: O(N)
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        # Time: O(log(N) | Space: O(n)
        def union(x, y, conn_comps):
            # Note immutable var (conn_comps) are available in nested function as read only
            xset = find(x)
            yset = find(y)

            if xset != yset:
                # **imp - since parents are different, connected components reduce by 1
                conn_comps -= 1
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:
                    parent[yset] = xset
                    rank[xset] += 1
            return conn_comps

        conn_comps = N
        # Define parent and rank
        parent = [i for i in range(N)]
        rank = [0 for _ in range(N)]

        # ** imp - why sort ?
        # 1. we want to find earliest log time that we have all friends connected and log times are not in order
        # 2. we cannot use min and O(n) scan in main for because lets say the last edge remaining is (5,6) and we come accross log entry (1000, 5, 6), we will return 1000 as ans. But suppose later in the log entries we have (500, 5, 6) as a log entry, correct ans wpuld be 500
        logs.sort()  # E*Log(E) - E is num of edges

        # Union find till we have 1 connected component
        for log, x, y in logs:
            conn_comps = union(x, y, conn_comps)
            if conn_comps == 1:
                return log

        return -1
