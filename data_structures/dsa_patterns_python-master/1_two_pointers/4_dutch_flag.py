# LeetCode: 75 - Sort Colors (Dutch National Flag)

# Time: O(n) | Space: O(1)
def dutch_flag_sort(nums):
    # Indexes point to where next 0 and 2 element should be put
    # all elements < next_zero should be 0, all elements > next_two should be 2
    # once we put 0 and 2 in their right places, 1 will automatically be in its right place
    next_zero, next_two = 0, len(nums) - 1
    i = 0
    # imp condition for termination
    while i <= next_two:
        if nums[i] == 0:
            # swap with element at next_zero index
            nums[next_zero], nums[i] = nums[i], nums[next_zero]
            # increment next_zero
            next_zero += 1
            # the element at next_zero has to be 1 ?
            # when we are at i all elements before i have been put in their correct place
            # so element at next_zero has to be 1
            # hence we can increment i also
            i += 1
        elif nums[i] == 2:
            # swap with element at next_two index
            nums[next_two], nums[i] = nums[i], nums[next_two]
            # decrement next_two
            next_two -= 1
            # since this element could be 0 or 2 we cannot move to next element
            # if after swapping this element becomes 0 we need to put it in its right place
        else:
            # arr[i] == 1
            i += 1

    return nums


def main():
    # arr = [1, 0, 2, 1, 0]
    # dutch_flag_sort(arr)
    # print(arr)

    nums = [2, 2, 0, 1, 2, 0]
    dutch_flag_sort(nums)
    print(nums)


main()
