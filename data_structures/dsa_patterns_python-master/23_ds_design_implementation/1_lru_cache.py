# Copyright © 2020 way2FAANG
# LeetCode: 146
# Level: med

class Node:
    # Double Linked List Node + hash map
    # Algorithm - Use Double Linked List as queue
    # - queue front to hold the most recently used key (node)
    # - queue end to hold lru key (node)
    # when we do a get or put at a key we remove the node and add it to fornt as it is the most recently used queue - hence we need a double linked list (remove has to be O(1) given reference to the node)

    def __init__(self, key, val):
        # We can store multiple data points at a LL node
        self.key = key
        self.val = val
        # We need double link
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_node_map = dict()
        self.head = Node(-100, -100)  # dummy node
        self.tail = Node(-100, -100)  # dummy node
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        # print(f"get -> {key}")

        node = self.key_node_map.get(key, None)
        if node is not None:
            self.remove(node)
            self.add_to_front(node)
            # self.printll()
            return node.val

        # self.printll()
        return -1

    def put(self, key: int, value: int) -> None:
        # print(f"put -> {key}, {value}")

        if key in self.key_node_map:
            self.remove(self.key_node_map.get(key))
        # create new node
        node = Node(key, value)
        self.add_to_front(node)  # pass by reference
        self.key_node_map[key] = node
        if len(self.key_node_map) > self.capacity:
            # imp - remove from hash map to
            del self.key_node_map[self.tail.prev.key]
            self.remove(self.tail.prev)

        # self.printll()

    def remove(self, node: Node) -> None:
        # print(f"remove->{node.val}, {node.next}, {node.prev}")
        # removes the node from Double LL
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next, node.prev = None, None  # ideally not needed, as this node is not referenced by any other object it should be garbage collected

    def add_to_front(self, node: Node):
        # first change node pointers
        node.prev = self.head
        node.next = self.head.next
        # then head and next for head
        self.head.next.prev = node
        self.head.next = node

    def printll(self):
        current = self.head
        while current:
            print(f"{current.val}->", end='')
            current = current.next
        print()

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
