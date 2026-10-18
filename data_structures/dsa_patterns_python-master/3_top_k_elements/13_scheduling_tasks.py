# Copyright © 2020 way2FAANG
# LeetCode: 621


from heapq import heappush, heappop
from collections import deque


# Time: O(n*log(n)) | Space: O(n)
# Use max heap to execute the task with max remaining freq first
# Use queue to keep a task out of max heap until its cooldown ends
# Unlike previous problem, track time instead of queue length since we can have idle intervals
def schedule_tasks(tasks, k):
    time = 0
    task_freq_map = {}
    for task in tasks:
        task_freq_map[task] = task_freq_map.get(task, 0) + 1

    max_heap = []
    for task, freq in task_freq_map.items():
        heappush(max_heap, (-freq, task))

    queue = deque()
    # Heap can be empty while unfinished tasks are still cooling down in queue
    while max_heap or queue:
        # If no task is available, skip idle intervals until the first task is ready
        if not max_heap:
            time = max(time, queue[0][2])

        # Tasks enter queue in time order, so the first task becomes ready first
        while queue and queue[0][2] <= time:
            prev_freq, prev_task, available_at = queue.popleft()
            heappush(max_heap, (prev_freq, prev_task))

        freq, task = heappop(max_heap)
        freq += 1  # decrement freq
        # Keep this task out of heap for the next k intervals
        # A task executed at time t can run again at t + k + 1
        if -freq > 0:
            queue.append((freq, task, time + k + 1))
        time += 1

    return time


def main():
    print("Minimum intervals needed to execute all tasks: " +
          str(schedule_tasks(['a', 'a', 'a', 'b', 'c', 'c'], 2)))
    print("Minimum intervals needed to execute all tasks: " +
          str(schedule_tasks(['a', 'b', 'a'], 3)))


main()

