# Copyright © 2020 way2FAANG
# LeetCode: 252


# Time: O(n*log(n) | Space: O(n) for sorting - Timsort
def can_attend_all_appointments(intervals):
    start, end = 0, 1
    intervals.sort(key=lambda x: x[start])

    for i in range(len(intervals) - 1):
        # 3 cases possible since sorted (a start before b)
        # intervals having condition "intervals[i][end] == intervals[i+1][start]"
        # don't cause conflict as one starts right after the other
        if intervals[i][end] > intervals[i + 1][start]:
            return False
    return True


def main():
    print("Can attend all appointments: " + str(can_attend_all_appointments([[1, 4], [2, 5], [7, 9]])))
    print("Can attend all appointments: " + str(can_attend_all_appointments([[6, 7], [2, 4], [8, 12]])))
    print("Can attend all appointments: " + str(can_attend_all_appointments([[4, 5], [2, 3], [3, 6]])))


main()
