# Time: O(N) time | Space: O(1)
def find_all_duplicates(nums):
    duplicateNumbers = set()
    current_index = 0
    while current_index < len(nums):
        # since numbers starting from 1
        correct_index = nums[current_index] - 1
        if nums[current_index] != nums[correct_index]:
            # swap
            nums[current_index], nums[correct_index] = nums[correct_index], nums[current_index]
        else:
            if current_index != correct_index:
                # duplicate
                duplicateNumbers.add(nums[current_index])
            current_index += 1

    return list(duplicateNumbers)


if __name__ == '__main__':
    print(find_all_duplicates([3, 4, 4, 5, 5]))
    print(find_all_duplicates([5, 4, 7, 2, 3, 5, 3]))

