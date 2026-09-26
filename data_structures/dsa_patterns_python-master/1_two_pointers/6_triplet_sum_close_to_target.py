# LeetCode: 16 - 3Sum Closest

# Time: O(n^2) | Space: O(n) auxiliary for Python sorting
def triplet_sum_close_to_target(arr, target_sum):
    # question check - array is unsorted
    arr.sort()

    # since we need to track min value, initial value should be max possible
    # why should we track min_diff, generally in triplets we use current_sum. So why can't we track sum_close_to_target
    # **answered in the for loop
    min_diff = float('inf')

    for i in range(len(arr) - 2):

        # search closest pairs
        left, right = i + 1, len(arr) - 1
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            # **how do we measure if this triplet is closer to target than current value of sum_close_to_target
            # we can measure how close current_sum is to target by calculating its difference with target
            # hence we track min_diff and not sum_closest_to_target
            current_diff = target_sum - current_sum
            if current_diff == 0:   # we've found a triplet with an exact sum, best case
                return current_sum  # in this case equal to target sum

            # update min diff
            if (abs(current_diff) < abs(min_diff)) or (abs(current_diff) == abs(min_diff) and current_diff > min_diff):
                min_diff = current_diff

            if current_sum < target_sum:
                left += 1
            else:
                right -= 1
    # for returning use eq: current_diff = target_sum - current_sum -> current_sum = target_sum - current_diff

    return target_sum - min_diff # sum_closest_to_target


if __name__ == '__main__':
    print(triplet_sum_close_to_target([-2, 0, 1, 2], 2))
    assert triplet_sum_close_to_target([-2, 0, 1, 2], 2) == 1, 'Test case 1 failed'
    print(triplet_sum_close_to_target([-3, -1, 1, 2], 1))
    print(triplet_sum_close_to_target([1, 0, 1, 1], 100))
