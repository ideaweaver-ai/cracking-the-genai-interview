"""Run all examples or one: python 10_standard_library_tools.py deque"""

from collections import deque
import heapq


def deque_example():
    queue = deque(["first", "second"])
    queue.append("third")
    print(queue.popleft())  # deque removes from either end in O(1) time.


def heap():
    priorities = [4, 1, 3]
    heapq.heapify(priorities)
    heapq.heappush(priorities, 2)
    print(heapq.heappop(priorities))


EXAMPLES = {"deque": deque_example, "heap": heap}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
