from random import randint
from . import run_sorting_algorithm


# Time: O(n) | Space: O(n)
def merge(left, right):
    """
    Merge two arrays
    :param left: Left array
    :param right: Right array
    :return: Returns the merged array
    """
    # If the first array is empty, then nothing needs
    # to be merged, and you can return the second array as the result
    if len(left) == 0:
        return right

    # If the second array is empty, then nothing needs
    # to be merged, and you can return the first array as the result
    if len(right) == 0:
        return left

    result = []
    index_left = index_right = 0

    # Now go through both arrays until all the elements
    # make it into the resultant array
    while len(result) < len(left) + len(right):
        # The elements need to be sorted to add them to the
        # resultant array, so you need to decide whether to get
        # the next element from the first or the second array
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        # If you reach the end of either array, then you can
        # add the remaining elements from the other array to
        # the result and break the loop
        if index_right == len(right):
            # right arr has ended
            result += left[index_left:]
            break

        if index_left == len(left):
            # left arr has ended
            result += right[index_right:]
            break

    return result


# Time: = O(log(n) -splitting + O(n)*log(n) - merging =  O(n*log(n)) | Space: O(n)
def merge_sort(array):
    # If the input array contains fewer than two elements,
    # then return it as the result of the function
    # base case
    if len(array) < 2:
        return array

    # recursive calls
    midpoint = len(array) // 2
    left_half = array[:midpoint]
    right_half = array[midpoint:]
    left_half_sorted = merge_sort(left_half)
    right_half_sorted = merge_sort(right_half)

    # Sort the array by recursively splitting the input
    # into two equal halves, sorting each half and merging them
    # together into the final result
    return merge(left_half_sorted, right_half_sorted)


if __name__ == "__main__":
    # Test case 1
    arr = [3, 7, 2, 1]
    print(f'{arr} sorted: {merge_sort([3, 7, 2, 1])}')
    assert merge_sort([3, 7, 2, 1]) == [1, 2, 3, 7], 'Incorrectly sorted'

    # Generate an array of `ARRAY_LENGTH` items consisting
    ARRAY_LENGTH = 1000
    # Generate an array of `ARRAY_LENGTH` items consisting
    # of random integer values between 0 and 999
    array = [randint(0, 1000) for i in range(ARRAY_LENGTH)]

    # Call the function using the name of the sorting algorithm
    # and the array you just created
    run_sorting_algorithm(algorithm="merge_sort", array=array)