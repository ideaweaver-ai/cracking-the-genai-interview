# Time: O(N) time | Space: O(1) space
def find_corrupt_numbers(nums):
    current_index = 0
    while current_index < len(nums):
        correct_index = nums[current_index] - 1
        if nums[current_index] != nums[correct_index]:
            # swap
            nums[current_index], nums[correct_index] = nums[correct_index], nums[current_index]
        else:
            # ** imp dont return here if current_index != correct_index
            # - we would have found the duplicate, but missing would be incorrect
            current_index += 1

    # find missing and duplicate
    for current_index in range(len(nums)):
        if nums[current_index] != current_index + 1:
            return [nums[current_index], current_index + 1]
    return [-1, -1]


if __name__ == '__main__':
    print(find_corrupt_numbers([3, 1, 2, 5, 2]))
    print(find_corrupt_numbers([3, 1, 2, 3, 6, 4]))
