from random import randint
# from sorting import run_sorting_algorithm


# Time: O(n**2) | Space: O(1)
def insertion_sort(array):
    # Loop from the second element of the array until
    # the last element
    for i in range(1, len(array)):
        # This is the element we want to position in its
        # correct place
        key_item = array[i]

        # Initialize the variable that will be used to
        # find the correct position of the element referenced
        # by `key_item`
        j = i - 1

        # Run through the list of items (the left
        # portion of the array) and find the correct position
        # of the element referenced by `key_item`. Do this only
        # if `key_item` is smaller than its adjacent values.
        while j >= 0 and array[j] > key_item:
            # Shift the value one position to the left
            # and reposition j to point to the next element
            # (from right to left)
            array[j + 1] = array[j]
            j -= 1

        # When you finish shifting the elements, you can position
        # `key_item` in its correct location
        array[j + 1] = key_item

    return array


if __name__ == '__main__':
    # Test case 1
    arr = [3, 7, 2, 1]
    print(f'{arr} sorted: {insertion_sort([3, 7, 2, 1])}')
    assert insertion_sort([3, 7, 2, 1]) == [1, 2, 3, 7], 'Incorrectly sorted'

    # Generate an array of `ARRAY_LENGTH` items consisting
    ARRAY_LENGTH = 1000
    # of random integer values between 0 and 999
    array = [randint(0, 1000) for i in range(ARRAY_LENGTH)]

    # Call the function using the name of the sorting algorithm
    # and the array you just created
    run_sorting_algorithm(algorithm="insertion_sort", array=array)
