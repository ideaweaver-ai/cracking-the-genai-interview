# Copyright © 2020 way2FAANG
# LeetCode: 380
# Level: medium

import random


class RandomizedSet:
    # Space: O(n)
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.num_list_index_map = dict()
        self.num_list = []

    # Time: O(1)
    def insert(self, val: int) -> bool:
        """
        Inserts a value to the set. Returns true if the set did not already contain the specified element.
        """
        if val in self.num_list_index_map:
            return False
        self.num_list.append(val)
        self.num_list_index_map[val] = len(self.num_list) - 1
        return True

    # Time: O(1)
    def remove(self, val: int) -> bool:
        """
        Removes a value from the set. Returns true if the set contained the specified element.
        """
        if val not in self.num_list_index_map: return False
        # get the index of the val in list and then delete
        index_in_list = self.num_list_index_map.get(val)
        # to prevent removal of last element giving error
        if index_in_list != len(self.num_list):
            # swap element at that index with last one so we can del element from list in O(1)
            self.num_list[-1], self.num_list[index_in_list] = self.num_list[index_in_list], self.num_list[-1]
            # update the index for the last element
            self.num_list_index_map[self.num_list[index_in_list]] = index_in_list
        self.num_list.pop()
        # remove from hash map
        del self.num_list_index_map[val]

        return True

    # Time: O(1)
    def getRandom(self) -> int:
        """
        Get a random element from the set.
        """
        if not self.num_list_index_map:
            return None
        return random.choice(self.num_list)

# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
