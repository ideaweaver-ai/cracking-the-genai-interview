# Copyright © 2020 way2FAANG
# LeetCode: 56


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def print_interval(self):
        print("[" + str(self.start) + ", " + str(self.end) + "]", end='')


# Time: O(n*log(n)) | Space: O(n) space for sorting
def merge(intervals):

    if not intervals or len(intervals) < 2:
        return intervals

    # Output var - merged intervals
    merged_intervals = []

    # Need to sort intervals on start time
    intervals.sort(key=lambda x: x.start)

    # next merged interval to append to o/p - doing this as we don't want to modify input
    prev_interval_start = intervals[0].start
    prev_interval_end = intervals[0].end

    # merge overlapping intervals one by one
    for i in range(1, len(intervals)):
        current_interval = intervals[i]
        # since intervals are sorted on start time, out of 6 only 3 cases possible - b after a
        # overlapping
        # if prev_interval_end >= current_interval.start :

        # can also use generic condition for a overlaps b
        if prev_interval_start <= current_interval.start <= prev_interval_end:

            # need to modify only end as start of a before b, hence only end needs to be updated
            # ** but even if you use generic ode for merging and update start it will still work correctly
            prev_interval_start = min(current_interval.start, prev_interval_start)
            prev_interval_end = max(current_interval.end, prev_interval_end)
        # not overlapping
        else:
            # add the current interval and reset
            merged_intervals.append(Interval(prev_interval_start, prev_interval_end))
            prev_interval_start, prev_interval_end = current_interval.start, current_interval.end

    # the last interval still needs to be merged. Do you understand this ?
    merged_intervals.append(Interval(prev_interval_start, prev_interval_end))

    return merged_intervals


def main():
    print("Merged intervals: ", end='')
    for i in merge([Interval(1, 4), Interval(2, 5), Interval(7, 9)]):
        i.print_interval()
    print()

    print("Merged intervals: ", end='')
    for i in merge([Interval(6, 7), Interval(2, 4), Interval(5, 9)]):
        i.print_interval()
    print()

    print("Merged intervals: ", end='')
    for i in merge([Interval(1, 4), Interval(2, 6), Interval(3, 5)]):
        i.print_interval()
    print()


main()