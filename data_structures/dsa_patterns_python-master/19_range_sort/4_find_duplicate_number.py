def find_duplicate(nums):
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
                return nums[current_index]
            current_index += 1
