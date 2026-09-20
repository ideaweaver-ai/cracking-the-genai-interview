# Copyright © 2020 way2FAANG
# LeetCode: 621


from heapq import heappush, heappop


# Time: O(n* log(n)) | Space: O(n)
# Why we don't use queue like previous problem ?
# Because in case when we have idle cycles, the queue length will not increase and we will exit the main while
# with tasks in queue scheduled
def schedule_tasks(tasks, k):
    intervalCount = 0
    task_freq_map = {}
    for task in tasks:
        task_freq_map[task] = task_freq_map.get(task, 0) + 1

    max_heap = []
    for task, freq in task_freq_map.items():
        heappush(max_heap, (-freq, task))

    wait_list = []
    while max_heap:
        tasks_to_complete_in_cycle = k + 1
        while tasks_to_complete_in_cycle > 0 and max_heap:
            freq, task = heappop(max_heap)
            intervalCount += 1
            tasks_to_complete_in_cycle -= 1
            freq += 1
            # In this case makes sense to push into wait list only if freq > 0
            if -freq > 0:
                wait_list.append((freq, task))

        if tasks_to_complete_in_cycle > 0 and wait_list:
            # idle cycles
            intervalCount += tasks_to_complete_in_cycle

        # we can add back the wait list task to max_heap
        # we can do this because we are just counting time to schedule the tasks
        # not actually returning sequence of schedule tasks -
        # in that case we will have to use queue to guarantee task is not executed during coolong period
        while wait_list:
            heappush(max_heap, wait_list.pop())

    return intervalCount


def main():
    print("Minimum intervals needed to execute all tasks: " +
          str(schedule_tasks(['a', 'a', 'a', 'b', 'c', 'c'], 2)))
    print("Minimum intervals needed to execute all tasks: " +
          str(schedule_tasks(['a', 'b', 'a'], 3)))


main()

