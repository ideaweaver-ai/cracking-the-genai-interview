class MinHeap:
    def __init__(self):
        self.heap = []

    # Time: O (log(n))
    def insert(self, val):
        self.heap.append(val)
        self.__percolate_up(len(self.heap)-1)

    # Time: O (log(n))
    def __percolate_up(self, index):
        parent_index = (index-1)//2
        if parent_index >= 0 and self.heap[index] < self.heap[parent_index]:
            # swap
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self.__percolate_up(parent_index)

    # Time: O (log(n))
    def __percolate_down(self, index):
        left_child_index, right_child_index = 2*index+1, 2*index+2
        smallest = index
        if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest]:
            smallest = left_child_index
        if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest]:
            smallest = right_child_index
        if smallest != index:  # one of the children has smaller value
            # swap
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.__percolate_down(smallest)

    # Time: O (log(1))
    def getMin(self):
        # Validate heap is not empty
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    # Time: O (log(n))
    def pop(self):
        # Validate heap is not empty
        if len(self.heap) == 0:
            return None

        temp = self.heap[0]
        self.heap[0] = self.heap[-1]

        del self.heap[-1]   # O(1)

        if len(self.heap) > 0:
            # Heapifying in case if original heap os of 1 len will give index error
            self.__percolate_down(0)

        return temp

    # Intutively seems O(n* log(n)), but it is O(n)
    def heapify(self, arr):
        self.heap = arr
        for i in range(len(self.heap)-1, -1, -1):
            self.__percolate_down(i)
heap = MinHeap()
heap.insert(12)
heap.insert(10)
heap.insert(-10)
heap.insert(100)

print(heap.getMin())
print(heap.pop())
print(heap.getMin())
heap.insert(-100)
print(heap.getMin())

print("Testing build heap")
heap.heapify([2, 8, -1, 5, -42, 9])
print(heap.heap)
print(heap.pop())
print(heap.heap)
print(heap.pop())
print(heap.heap)
print(heap.pop())