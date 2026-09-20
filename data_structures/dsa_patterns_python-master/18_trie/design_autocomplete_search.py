# Copyright © 2020 way2FAANG
# LeetCode: 642

from typing import List


# Hash map solution (Brute Force)
# class AutocompleteSystem:
#     # k - number of historical entries, l - avg length in characters of sentence/string
#     # Time : O(k*l) | Space: O(k*l)
#     def __init__(self, sentences: List[str], times: List[int]):
#         self.hash_map = {}
#         # for i in range(len(sentences)):
#         #     self.hash_map[sentences[i]] = times[i]
#         for sentence, time in zip(sentences, times):
#             self.hash_map[sentence] = time
#         # store user input sentence
#         self.current_user_sentence = []
#
#     # n - number of entries in the map | Why different from k - because we add user input to the entries
#     # m - avg number of matches (sentences/ strings)
#     # Time : O(n*l + (m*l)*log(m*l))
#     def input(self, c: str) -> List[str]:
#         # add current char to user's current sentence being inputted
#         self.current_user_sentence.append(c)
#
#         # store the result - matched sentences
#         result = {}
#         # find any sentence that matches the current input
#         for sentence, hotness in self.hash_map.items():
#             match_found = True
#             for i in range(len(self.current_user_sentence)):
#                 if i >= len(sentence) or self.current_user_sentence[i] != sentence[i]:
#                     # mismatch
#                     match_found = False
#                     break
#             # add to result if match found
#             if match_found:
#                 result[sentence] = hotness
#
#         # sort the result
#         # first sort alphabetically to resolve ties
#         result = sorted(result.items())  # now result is a list of tuples
#         result = sorted(result, key=lambda x: x[1], reverse=True)
#         result = [sent for sent, _ in result]
#
#         # if end of sentence, add to historical data
#         if c == '#':
#             # convert the list into string
#             current_user_sentence_completed = ''.join(self.current_user_sentence[:-1])
#             # increase the hotness by 1
#             self.hash_map[current_user_sentence_completed] = self.hash_map.get(current_user_sentence_completed, 0) + 1
#             # new search query
#             self.current_user_sentence = []
#
#         return result[:3]


# Trie solution
# class TrieNode:
#     def __init__(self):
#         self.children = {}
#         self.is_end = False
#         self.data = None  # we will store complete sentence at the node where the sentence ends
#         self.rank = 0
#
#
# class AutocompleteSystem:
#     # k - number of historical entries, l - avg length of sentence
#     # Time : O(k*l) | Space: O(k*l)
#     def __init__(self, sentences: List[str], times: List[int]):
#         # Create root of out Trie
#         self.root = TrieNode()
#         # add sentences to the Trie
#         for sentence, hotness in zip(sentences, times):
#             self.insert(sentence, hotness)
#         # init a variable to track user input
#         self.input_phrase = []
#
#     def insert(self, sentence, hotness):
#         current_node = self.root
#         for char in sentence:
#             if char not in current_node.children:
#                 current_node.children[char] = TrieNode()
#             current_node = current_node.children[char]
#         # sentence ends, store complete sentence, mark end and add rank
#         current_node.is_end = True
#         current_node.data = sentence
#         current_node.rank -= hotness
#
#     # n - number of entries in the map | Why different from k - because we add user input to the entries
#     # m - avg number of matches
#     # p - length of the input phrase from user
#     # Time : O(p + (m*l)*log(m*l))
#     def search(self, input_phrase):
#         result = []
#         current_node = self.root
#         for char in input_phrase:
#             if char not in current_node.children:
#                 return result  # empty result
#             current_node = current_node.children[char]
#         # the input phrase is found
#         # we can start adding results
#         # ** imp - we only need to add complete sentences with these phrases as results
#         self.dfs(current_node, result)
#         return result
#
#     def dfs(self, current_node, result):
#         # base cases - ideally not needed as for loop takes care
#         if not current_node:  # None
#             return
#
#         # process current node
#         # if current node is where a sentence ends, add to result
#         if current_node.is_end:
#             result.append((current_node.rank, current_node.data))
#
#         # recursive calls
#         for char, child in current_node.children.items():
#             self.dfs(child, result)
#
#     def input(self, c: str) -> List[str]:
#         result = []
#         if c != "#":
#             self.input_phrase.append(c)
#             result = self.search("".join(self.input_phrase))
#             # sort and trim to 3 results
#             # For same rank, result is already sorted alphabetically as we are going in order for children
#             result = [sentence for _, sentence in sorted(result)[:3]]
#         else:
#             # add sentence to historical records
#             self.insert("".join(self.input_phrase),
#                         1)  # since we took care of adding (subtracting) hotness in insert we can do this
#             self.input_phrase = []
#         return result


# Optimized Trie solution
class TrieNode:
    def __init__(self):
        self.children = {}
        self.sentence = None  # will store the sentence where it is completed, alos helps to identify end of sentence
        self.hotness = 0


class AutocompleteSystem:
    # k - number of historical entries, l - avg length of sentence
    #     # Time : O(k*l) | Space: O(k*l)
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = TrieNode()
        for i in range(len(sentences)):
            sentence = sentences[i]
            hotness = times[i]
            self._insert(sentence, hotness)
        self.current_sentence = []
        self.last_search_node = self.root

    def _insert(self, sentence, hotness):
        current_node = self.root
        for char in sentence:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.sentence = sentence  # sentence complete
        current_node.hotness += hotness

    def _dfs(self, current_node, result):
        # base cases
        if current_node.sentence is not None:
            result.append((-current_node.hotness, current_node.sentence))

        for child_char, child_node in current_node.children.items():
            self._dfs(child_node, result)

    def _find_children_sentences(self, start_node):
        result = []
        self._dfs(start_node, result)
        return result

    # n - number of entries in the map | Why different from k - because we add user input to the entries
    # m - avg number of matches
    # p - length of the input phrase from user
    # Time : O((m*l)*log(m*l))
    def input(self, c: str) -> List[str]:
        if c == "#":
            self.last_search_node.sentence = "".join(self.current_sentence)
            self.last_search_node.hotness += 1
            self.last_search_node = self.root
            self.current_sentence = []
            return []

        self.current_sentence.append(c)
        # print(c, self.last_search_node.children)
        if c not in self.last_search_node.children:
            self.last_search_node.children[c] = TrieNode()
        self.last_search_node = self.last_search_node.children[c]
        result = self._find_children_sentences(self.last_search_node)
        result.sort()  # sorted based on descendong order of hotness
        # print(result)
        result = [sentence for hotness, sentence in result]
        return result[:3]
