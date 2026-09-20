from heapq import heappush, heappop


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end


# Time: O(n*log(n)) | Space: O(n)
def find_next_interval(intervals):
    result = [-1 for _ in range(len(intervals))]
    endHeap, startHeap = [], []  # both min heaps
    for i in range(len(intervals)):
        heappush(endHeap, (intervals[i].end, i))
        heappush(startHeap, (intervals[i].start, i))

    for _ in range(len(intervals)):
        current_end, current_index = heappop(endHeap)
        # break condition - startHeap becomes empty or found next interval for current element
        while startHeap and startHeap[0][0] < current_end:
            heappop(startHeap)
        # startHeap is empty
        if not startHeap:
            break
        # found next interval
        next_interval_start, next_interval_index = startHeap[0]
        result[current_index] = next_interval_index
    return result


def main():
    result = find_next_interval(
        [Interval(2, 3), Interval(3, 4), Interval(5, 6)])
    print("Next interval indices are: " + str(result))

    result = find_next_interval(
        [Interval(3, 4), Interval(1, 5), Interval(4, 6)])
    print("Next interval indices are: " + str(result))


main()
