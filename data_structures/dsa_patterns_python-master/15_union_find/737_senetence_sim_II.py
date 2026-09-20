from typing import List


class Solution:
    def areSentencesSimilarTwo(self, words1: List[str], words2: List[str], pairs: List[List[str]]) -> bool:

        # Time: O(log(n)), Amortized: O(1)
        def find(i):
            # set default parent and rank if not present (first time the vertex is iterated)
            parent.setdefault(i, i)
            rank.setdefault(i, 0)

            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        def union(x, y):
            # default parent and rank are set in find
            xset = find(x)
            yset = find(y)

            if xset != yset:
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:
                    parent[yset] = xset
                    rank[xset] += 1

        # sentences should have same num of words
        if len(words1) != len(words2):
            return False

        parent = {}
        rank = {}

        for w1, w2 in pairs:
            union(w1, w2)

        for w1, w2 in zip(words1, words2):
            if find(w1) != find(w2):
                return False

        return True
