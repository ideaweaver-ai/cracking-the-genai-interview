# Copyright © 2020 way2FAANG
# LeetCode: 253


from heapq import *


class Meeting:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        # min heap based on ending time
        return self.end < other.end

# Algorithm
# Consider how would you do it normally
# when a new meeting has to be scheduled:
# if any of the earlier meetings has ended schedule it in that room -
#       hence we need to find all earlier meetings having end time <= current meetings start time
#       so we need to keep track of end time of meetings
#       what's an efficient ds to give an earlier meeting with min end time
# else allot a new room

# ** key insight
# while scheduling current meeting, remove all the meetings (from calendar) ending before current meeting starts.


# Time: O(N*log(N)) | Space: O(N) for min_heap
def min_meeting_rooms(meetings):
    # o/p var
    min_rooms = 0

    # sort meetings based on start
    # because while scheduling current meeting we want to compare with earlier meetings
    meetings.sort(key=lambda x: x.start)

    # min_heap holds all the currently active meetings
    min_heap = []
    for current_meeting in meetings:
        # remove all the meetings that have ended
        while min_heap and min_heap[0].end <= current_meeting.start:
            heappop(min_heap)
        # add the current meeting into min_heap (schedule current meeting)
        heappush(min_heap, current_meeting)
        # all active meetings are in the min_heap now, so we need rooms for all of them.
        # current num of meeting rooms = len(min_heap)
        min_rooms = max(min_rooms, len(min_heap))
    return min_rooms


def main():
    print("Minimum meeting rooms required: " + str(min_meeting_rooms(
        [Meeting(4, 5), Meeting(2, 3), Meeting(2, 4), Meeting(3, 5)])))
    print("Minimum meeting rooms required: " +
          str(min_meeting_rooms([Meeting(1, 4), Meeting(2, 5), Meeting(7, 9)])))
    print("Minimum meeting rooms required: " +
          str(min_meeting_rooms([Meeting(6, 7), Meeting(2, 4), Meeting(8, 12)])))
    print("Minimum meeting rooms required: " +
          str(min_meeting_rooms([Meeting(1, 4), Meeting(2, 3), Meeting(3, 6)])))
    print("Minimum meeting rooms required: " + str(min_meeting_rooms(
        [Meeting(4, 5), Meeting(2, 3), Meeting(2, 4), Meeting(3, 5)])))


main()
