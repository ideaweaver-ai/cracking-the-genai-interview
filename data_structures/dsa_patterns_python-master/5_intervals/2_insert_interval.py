# Copyright © 2020 way2FAANG
# LeetCode: 57

# Algorithm
# 1 - find position where to insert
# 2 - merge intervals one by one

# Time: O(n) | Space: O(n) including o/p, O(1) excluding o/p
def insert(intervals, new_interval):
    # I/p validation
    if not new_interval:
        return intervals

    # o/p var
    merged_intervals = []
    # constants for better readability
    start, end = 0, 1

    # find correct position where new interval needs to be inserted
    # add all the intervals we are skipping to merged_intervals
    i = 0
    while i < len(intervals) and new_interval[start] > intervals[i][end]:
        merged_intervals.append(intervals[i])
        i += 1

    # since start of a (new_interval) before end of b (intervals[i]) - 5 cases possible
    # only case non overlapping b.start > a.end
    # merge intervals if overlapping
    prev_interval_start, prev_interval_end = new_interval[start], new_interval[end]
    # generic condition will also work - in this case a can overlap b or b can overlap a

    # while i < len(intervals) and prev_interval_end >= intervals[i][start]:
    while i < len(intervals) and (prev_interval_start <= intervals[i][start] <= prev_interval_end or intervals[i][
        start] <= prev_interval_start <= intervals[i][end]):
        # ** imp - change from prev prob, start can be either the interval start or merged interval start
        # generically calculate start and end of the merged interval
        prev_interval_start = min(prev_interval_start, intervals[i][start])
        prev_interval_end = max(prev_interval_end, intervals[i][end])
        i += 1

    # append last interval
    merged_intervals.append([prev_interval_start, prev_interval_end])

    # append remaining intervals
    while i < len(intervals):
        merged_intervals.append([intervals[i][start], intervals[i][end]])
        i += 1

    return merged_intervals


def main():
    print("Intervals after inserting the new interval: " + str(insert([[1, 3], [5, 7], [8, 12]], [4, 6])))
    print("Intervals after inserting the new interval: " + str(insert([[1, 3], [5, 7], [8, 12]], [4, 10])))
    print("Intervals after inserting the new interval: " + str(insert([[2, 3], [5, 7]], [1, 4])))


main()
