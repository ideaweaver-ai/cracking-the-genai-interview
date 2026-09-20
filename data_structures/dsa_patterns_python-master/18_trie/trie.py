# Assumptions 'n' keys/ words stored in 21_trie/ avg length of a word - 'm'

class TrieNode:
    def __init__(self):
        self.children = {}  # we can use default dict too
        self.is_end = False


class Trie:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    # Wost case time: O(n*m) | Worst case space: O(n*m)
    # but ideally since a lot of words will hae common prefix, the space ocmplexity will be smaller
    def insert(self, word: str) -> None:
        """
        Inserts a word into the 21_trie.
        """
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]

        # mark word end
        current_node.is_end = True

    # Wost case time: O(l) | Worst case space: O(n*m)
    def search(self, word: str) -> bool:
        """
        Returns if the complete word is in the 21_trie.
        """
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        # check if the cursor has word end
        return True if current_node.is_end else False

    # Wost case time: O(l) | Worst case space: O(n*m) - better than hashmap
    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the 21_trie that starts with the given prefix.
        """
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True

# Compare with hash map. Worst case TC and SC will be same.
# Advantages of Trie - 1.Actual space complexity will be smaller. 2. We can search for prefix

if __name__ == '__main__':
    trie = Trie()
    trie.insert('apple')
    trie.insert('bat')
    # TC1
    assert trie.search('apple') is True, "Test case 1 failed"
    assert trie.search('bat') is True, "Test case 2 failed"
    assert trie.search('cat') is False, "Test case 3 failed"