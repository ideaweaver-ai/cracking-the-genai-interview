# Time: O(N) | O(1) space
def find_missing_number(nums):
    # use range sort logic to put numbers in their correct index
    # **imp - handle n correctly so we don't get index error
    current_index = 0
    while current_index < len(nums):
        correct_index = nums[current_index]
        # imp - 'n' does not have a correct position, so no need to swap
        if correct_index < len(nums) and nums[correct_index] != nums[current_index]:
            # swap
            nums[correct_index], nums[current_index] = nums[current_index], nums[correct_index]
        else:
            current_index += 1

    # find the missing number - not equalling its index
    for current_index in range(len(nums)):
        if nums[current_index] != current_index:
            return current_index

    # since we reached this line, n must be the missing number
    return len(nums)


if __name__ == '__main__':
    print(find_missing_number([4, 0, 3, 1]))
    print(find_missing_number([8, 3, 5, 2, 4, 6, 0, 1]))
    print(find_missing_number([3, 0, 2, 1]))

