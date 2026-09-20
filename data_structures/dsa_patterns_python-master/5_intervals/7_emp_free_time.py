# Copyright © 2020 way2FAANG
# LeetCode: 759

from __future__ import print_function
from heapq import heappush, heappop


# class Interval:
#     def __init__(self, start, end):
#         self.start = start
#         self.end = end
#
#     def print_interval(self):
#         print("[" + str(self.start) + ", " + str(self.end) + "]", end='')
#
#
# class EmployeeInterval:
#     def __init__(self, interval, emp_index, interval_index):
#         self.interval = interval
#         self.emp_index = emp_index
#         self.interval_index = interval_index
#
#     def __lt__(self, other):
#         return self.interval.start < other.interval.start
#
#
# # Using sorting
# # Add all intervals to a list, sort them and use our merge logic to find free time (between consecutive intervals)
# # vars for time cpmplexity
# # m - num of intervals/ employee, e = num of employees. so total num of intervals = n*e
# # Time: O( (m*e) * log(m*e) time | Space: O(m*e) for sorting. n - total num of intervals
#
#
# # Improved algo
# # Use the fact - for each employee intervals are sorted
# # use a min heap to store the earliest interval for each employee
# # compare the 2 earliest intervals for free time
# # pop out the earliest interval and replace it with that employees next interval
# # Hence we need EmployeeInterval class for min heap
#
# # Time: O( (m*e) * log(m)) | Space O(m)
# def find_employee_free_time(schedule):
#     result = []
#     num_emps = len(schedule)
#     min_heap = []
#     for i in range(num_emps):
#         emp_interval = EmployeeInterval(schedule[i][0], i, 0)
#         heappush(min_heap, emp_interval)
#
#     previous_interval = min_heap[0].interval
#     while min_heap:
#         current_emp_interval = heappop(min_heap)
#         # no overlap - free time
#         if previous_interval.end < current_emp_interval.interval.start:
#             result.append(Interval(previous_interval.end,
#                                    current_emp_interval.interval.start))
#             previous_interval = current_emp_interval.interval
#         # overlapping - no free time
#         # does previous interval need to be updated ?
#         else:
#             if current_emp_interval.interval.end > previous_interval.end:
#                 previous_interval = current_emp_interval.interval
#
#         # we need to put back in min heap
#         # next interval for the employee whose interval was popped from min_heap
#         emp_schedule = schedule[current_emp_interval.emp_index]
#         interval_index_for_emp = current_emp_interval.interval_index
#         if interval_index_for_emp + 1 < len(emp_schedule):
#             heappush(min_heap, EmployeeInterval(emp_schedule[interval_index_for_emp + 1],
#                                                 current_emp_interval.emp_index, interval_index_for_emp + 1))
#
#     return result


# # Using sorting
# # Add all intervals to a list, sort them and use our merge logic to find free time (between consecutive intervals)
# # vars for time complexity
# # m - num of intervals/ employee, e = num of employees. so total num of intervals = n*e
# # Time: O( (m*e) * log(m*e) time | Space: O(m*e) for sorting. n - total num of intervals

# Using heap
# # Time: O( (m*e) * log(e)) | Space O(e)
class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.start < other.start

    def print_interval(self):
        print("[" + str(self.start) + ", " + str(self.end) + "]", end='')


def find_employee_free_time(schedule):
    # o/p var
    free_times = []

    # to find the earliest interval amongst all the employees
    min_heap = []
    for emp_num in range(len(schedule)):
        heappush(min_heap, (schedule[emp_num][0], emp_num, 0))

    # get the first interval to start merging
    prev_interval = min_heap[0][0]  # remember  heap consists a tuple

    while min_heap:
        current_interval, emp_num, interval_index = heappop(min_heap)
        # since intervals will be available in order of start time only 3 cases possible (a overlaps b)
        if prev_interval.end >= current_interval.start:
            # No free time, what end should we consider for next iteration ???
            prev_interval.end = max(prev_interval.end, current_interval.end)
        else:
            # not overlapping
            free_time_start = prev_interval.end
            free_time_end = current_interval.start

            free_times.append(Interval(free_time_start, free_time_end))
            prev_interval = current_interval
        # push the next interval of the popped employee into heap if it exists **
        if interval_index + 1 < len(schedule[emp_num]):
            heappush(min_heap, (schedule[emp_num][interval_index + 1], emp_num, interval_index + 1))

    return free_times


def main():
    input = [[Interval(1, 3), Interval(5, 6)], [
        Interval(2, 3), Interval(6, 8)]]
    print("Free intervals: ", end='')
    for interval in find_employee_free_time(input):
        interval.print_interval()
    print()

    input = [[Interval(1, 3), Interval(9, 12)], [
        Interval(2, 4)], [Interval(6, 8)]]
    print("Free intervals: ", end='')
    for interval in find_employee_free_time(input):
        interval.print_interval()
    print()

    input = [[Interval(1, 3)], [
        Interval(2, 4)], [Interval(3, 5), Interval(7, 9)]]
    print("Free intervals: ", end='')
    for interval in find_employee_free_time(input):
        interval.print_interval()
    print()


main()
