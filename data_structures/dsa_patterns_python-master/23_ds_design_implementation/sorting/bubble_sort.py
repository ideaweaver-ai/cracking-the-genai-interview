from random import randint
# from sorting import run_sorting_algorithm


# simple bubble sort
# Time: O(n**2) | Space: O(1)
def bubble_sort(array):
    n = len(array)

    for i in range(n):

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                array[j], array[j + 1] = array[j + 1], array[j]

    return array


# efficient bubble sort - stop if array is already sorted
# Time: O(n**2) | Space: O(1)
def bubble_sort(array):
    n = len(array)

    for i in range(n):
        # Create a flag that will allow the function to
        # terminate early if there's nothing left to sort
        already_sorted = True

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                array[j], array[j + 1] = array[j + 1], array[j]

                # Since you had to swap two elements,
                # set the `already_sorted` flag to `False` so the
                # algorithm doesn't finish prematurely
                already_sorted = False

        # If there were no swaps during the last iteration,
        # the array is already sorted, and you can terminate
        if already_sorted:
            break

    return array


if __name__ == '__main__':
    # Test case 1
    arr = [3, 7, 2, 1]
    print(f'{arr} sorted: {bubble_sort([3, 7, 2, 1])}')
    assert bubble_sort([3, 7, 2, 1]) == [1, 2, 3, 7], 'Incorrectly sorted'

    # Generate an array of `ARRAY_LENGTH` items consisting
    ARRAY_LENGTH = 1000
    # of random integer values between 0 and 999
    array = [randint(0, 1000) for i in range(ARRAY_LENGTH)]

    # Call the function using the name of the sorting algorithm
    # and the array you just created
    run_sorting_algorithm(algorithm="bubble_sort", array=array)

