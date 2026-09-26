# LeetCode: 26 - Remove Duplicates from Sorted Array

# Time: O(n) | Space: O(1)
def remove_duplicates(nums):
    # Placeholder to track where next unique num should be placed
    next_unique_num_index = 1

    for i in range(1, len(nums)):
        # When we find a unique num, place it at next_unique_index and increment index by 1
        if nums[i] != nums[i - 1]:
            nums[next_unique_num_index] = nums[i]
            next_unique_num_index += 1
    return next_unique_num_index


def main():
    print(remove_duplicates([2, 3, 3, 3, 6, 9, 9]))
    print(remove_duplicates([2, 2, 2, 11]))


main()
