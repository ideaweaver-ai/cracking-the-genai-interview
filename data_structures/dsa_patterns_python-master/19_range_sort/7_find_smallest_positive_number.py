# Time: O(N) | Space: O(1)
def find_first_missing_positive(nums):
    n = len(nums)
    current_index = 0
    while current_index < n:
        if nums[current_index] <= 0:
            # no need to sort non positive nums
            current_index += 1
            continue
        # we will sort nums > 0 (positive nums)
        correct_index = nums[current_index] - 1
        if correct_index < n and nums[current_index] != nums[correct_index]:
            # swap
            nums[current_index], nums[correct_index] = nums[correct_index], nums[current_index]
        else:
            current_index += 1

    for current_index in range(n):
        if nums[current_index] != current_index + 1:
            return current_index + 1

    return n + 1


if __name__=='__main__':
    # print(find_first_missing_positive([-3, 1, 5, 4, 2]))
    # print(find_first_missing_positive([3, -2, 0, 1, 2]))
    # print(find_first_missing_positive([3, 2, 5, 1]))
    print(find_first_missing_positive([3, 2, 4, 1]))
