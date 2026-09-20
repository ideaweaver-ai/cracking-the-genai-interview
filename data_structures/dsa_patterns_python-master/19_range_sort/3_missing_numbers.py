# Time: O(N) | Space: O(1)
def find_missing_numbers(nums):
    missingNumbers = []
    current_index = 0
    while current_index < len(nums):
        correct_index = nums[current_index] - 1
        # our logic handles duplicates
        if nums[current_index] != nums[correct_index]:
            # swap
            nums[current_index], nums[correct_index] = nums[correct_index], nums[current_index]
        else:
            current_index += 1

    for current_index in range(len(nums)):
        if nums[current_index] != current_index + 1:
            missingNumbers.append(current_index + 1)
    return missingNumbers
