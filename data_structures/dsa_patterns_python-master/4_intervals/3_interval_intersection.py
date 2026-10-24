# Copyright © 2020 way2FAANG
# LeetCode: 986


# Time: O(min(m,n))  n - len of a, m - len of b | Space: O(1) - excluding output
def merge(intervals_a, intervals_b):
    result = []
    start, end = 0, 1
    index_a, index_b = 0, 0
    while index_a < len(intervals_a) and index_b < len(intervals_b):
        # all 6 cases possible
        # most generic cases
        # a overlapping b - 2 cases
        # b start should be between a's start and end
        a_overlaps_b = intervals_a[index_a][start] <= intervals_b[index_b][start] <= intervals_a[index_a][end]
        # b overlapping a - 2 cases
        # a start should be between b's start and end
        b_overlaps_a = intervals_b[index_b][start] <= intervals_a[index_a][start] <= intervals_b[index_b][end]

        # add intersection to result
        if a_overlaps_b or b_overlaps_a:
            intersection_start = max(intervals_a[index_a][start], intervals_b[index_b][start])
            intersection_end = min(intervals_a[index_a][end], intervals_b[index_b][end])
            result.append([intersection_start, intersection_end])

        # we need to move only one interval pointer in one iteration ? do you understand this
        # which one do we move - 2 options. 1 interval which starts earlier. 2. interval which ends earlier
        # eg. if interval_a ends early we want to move index_a,
        # because start of next interval_a can still have intersection with the current interval_b
        if intervals_a[index_a][end] < intervals_b[index_b][end]:
            index_a += 1
        else:
            index_b += 1
    return result



def main():
    print("Intervals Intersection: " + str(merge([[1, 3], [5, 6], [7, 9]], [[2, 3], [5, 7]])))
    print("Intervals Intersection: " + str(merge([[1, 3], [5, 7], [9, 12]], [[5, 10]])))


main()
