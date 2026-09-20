from heapq import *


class Job:
    def __init__(self, start, end, cpu_load):
        self.start = start
        self.end = end
        self.cpu_load = cpu_load

    def __lt__(self, other):
        return self.end < other.end


# Time: O(n*log(n)) | Space: O(n)
def find_max_cpu_load(jobs):
    # o/p var and current load
    max_load, current_load = 0, 0

    # need to sort ?
    # when starting a new Job to see which of earlier jobs ended
    jobs.sort(key=lambda x: x.start)

    # will hold the current list of jobs
    min_heap = []

    for current_job in jobs:
        # remove jobs that have ended before current job
        while min_heap and min_heap[0].end <= current_job.start:
            finished_job = heappop(min_heap)
            current_load -= finished_job.cpu_load

        # add current Job to min heap and update current cpu load
        # the min heap has all current ongoing jobs now
        heappush(min_heap, current_job)
        current_load += current_job.cpu_load

        # update max_load
        max_load = max(max_load, current_load)
    return max_load


def main():
    print("Maximum CPU load at any time: " + str(find_max_cpu_load([Job(1, 4, 3), Job(2, 5, 4), Job(7, 9, 6)])))
    print("Maximum CPU load at any time: " + str(find_max_cpu_load([Job(6, 7, 10), Job(2, 4, 11), Job(8, 12, 15)])))
    print("Maximum CPU load at any time: " + str(find_max_cpu_load([Job(1, 4, 2), Job(2, 4, 1), Job(3, 6, 5)])))


main()
