import math


def count_min_jumps(jumps):
    def count_min_jumps_helper(i):
        """Returns min number of jumps from 'i' to reach the end of the array"""
        # base cases
        if i == n - 1:
            return 1

        # recursive calls
        max_jump_size_from_i = jumps[i]
        min_jumps_to_array_end_from_next_i = float('inf')
        for j in range(1, max_jump_size_from_i):
            if i + j < n:
                min_jumps_to_array_end_from_next_i = min(min_jumps_to_array_end_from_next_i,
                                                         count_min_jumps_helper(i + j))

        return min_jumps_to_array_end_from_next_i + 1

    # main function
    n = len(jumps)

    return count_min_jumps_helper(0)


def main():
    print(count_min_jumps([2, 1, 1, 1, 4]))
    print(count_min_jumps([1, 1, 3, 6, 9, 3, 0, 1, 3]))


main()