from collections import defaultdict
from typing import List


class Solution:
    def areSentencesSimilar(self, words1: List[str], words2: List[str], pairs: List[List[str]]) -> bool:
        # num of words in the two sentences are not equal
        if len(words1) != len(words2):
            return False

        # imp we need a set because a word can have many similar words
        pairs_map = defaultdict(set)

        for w1, w2 in pairs:
            pairs_map[w1].add(w2)
            pairs_map[w2].add(w1)

        # since we need to check sim of word1[i] only with word2[i]
        # zip will create a new list of [[word1[i], word2[i]]]
        for w1, w2 in zip(words1, words2):
            if w1 != w2 and w2 not in pairs_map[w1]:
                return False
        return True

