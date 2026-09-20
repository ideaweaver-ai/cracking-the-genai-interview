# Time: O(n+k) | Space: O(n) for extra nums
def find_first_k_missing_positive(nums, k):
    missingNumbers = []
    # Put positive numbers in the array in their correct place using cyclic sort
    # If positive num is >= than length of array add it to extra_nums dict
    # So we dont include those nums in the case k missing nums are not fulfilled by end of nums
    current_index = 0
    extra_nums = set()
    while current_index < len(nums):
        if nums[current_index] <= 0:
            # No need to change place of negative and 0
            current_index += 1
            continue

        correct_index = nums[current_index] - 1
        # check if number is out of nums length
        if correct_index >= len(nums):
            extra_nums.add(nums[current_index])
            current_index += 1
            continue

        if nums[current_index] != nums[correct_index]:
            # swap
            nums[current_index], nums[correct_index] = nums[correct_index], nums[current_index]
        else:
            current_index += 1
    # print(nums)

    # add missing positive nos
    for current_index in range(len(nums)):
        if len(missingNumbers) == k:
            break
        if nums[current_index] != current_index + 1:
            missingNumbers.append(current_index + 1)

    missing_num = len(nums) + 1
    while len(missingNumbers) < k:
        if missing_num not in extra_nums:
            missingNumbers.append(missing_num)
        missing_num += 1

    return missingNumbers


def main():
    print(find_first_k_missing_positive([3, -1, 4, 5, 5], 3))
    print(find_first_k_missing_positive([2, 3, 4], 3))
    print(find_first_k_missing_positive([-2, -3, 4], 2))


main()
