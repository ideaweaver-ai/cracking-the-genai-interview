# ** remember: heapify an arr of size n
# Intutively seems O(n* log(n)), but it is O(n)

class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, val):
        self.heap.append(val)
        self.__percolateUp(len(self.heap) - 1)

    def getMax(self):
        return self.heap[0]

    def remove_max(self):
        temp = self.heap[0]
        self.heap[0] = self.heap[-1]
        del self.heap[-1]  # O(1)
        self.__maxHeapify(0)
        return temp

    def __percolateUp(self, index):
        while True:
            parent_index = (index - 1) // 2
            if parent_index >= 0 and self.heap[index] > self.heap[parent_index]:
                # swap
                self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
                index = parent_index
            else:
                break

    def __maxHeapify(self, index):
        # Their code is cleaner
        while True:
            left_child_index, right_child_index = 2 * index + 1, 2 * index + 2
            if left_child_index >= len(self.heap):  # no children
                break
            elif right_child_index >= len(self.heap):
                # check only with left child (other case only right child present not possible as heap is complete tree)
                if self.heap[index] >= self.heap[left_child_index]:
                    break
                else:
                    self.heap[index], self.heap[left_child_index] = self.heap[left_child_index], self.heap[index]
                    index = left_child_index
            else:
                # both children present
                if self.heap[index] >= self.heap[left_child_index] and self.heap[index] >= self.heap[right_child_index]:
                    break
                else:
                    if self.heap[left_child_index] >= self.heap[right_child_index]:  # to swap with left child when both are equal
                        max_child_index = left_child_index
                    else:
                        max_child_index = right_child_index
                    # swap
                    self.heap[index], self.heap[max_child_index] = self.heap[max_child_index], self.heap[index]
                    index = max_child_index


heap = MaxHeap()
heap.insert(12)
heap.insert(10)
heap.insert(13)
heap.insert(100)

print(heap.getMax())
print(heap.heap)

