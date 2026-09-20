#  Time: worst case N-1 swaps and O(N) iteration = O(N) | Space: O(1)
def cyclic_sort(nums):
    current_index = 0
    while current_index < len(nums):
        correct_index = nums[current_index] - 1
        # why we check nums at the two indices and not correct_index != current_index?
        # because it handles duplicates better
        if nums[correct_index] != nums[current_index]:
            # num at current index is not at its correct index
            nums[correct_index], nums[current_index] = nums[current_index], nums[correct_index]
        else:
            current_index += 1

    return nums


def main():
    print(cyclic_sort([3, 1, 5, 4, 2]))
    print(cyclic_sort([2, 6, 4, 3, 1, 5]))
    print(cyclic_sort([1, 5, 6, 4, 3, 2]))


main()
