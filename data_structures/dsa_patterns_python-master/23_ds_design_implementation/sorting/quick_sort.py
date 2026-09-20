from random import randint
# from sorting import run_sorting_algorithm


# Time: Avg: O(n*log(n)), Worst Case: O(n**2) | Space: O(n)
def quicksort(array):
    # If the input array contains fewer than two elements,
    # then return it as the result of the function
    if len(array) < 2:
        return array

    low, same, high = [], [], []

    # Select your `pivot` element randomly
    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        # Elements that are smaller than the `pivot` go to
        # the `low` list. Elements that are larger than
        # `pivot` go to the `high` list. Elements that are
        # equal to `pivot` go to the `same` list.
        if item < pivot:
            low.append(item)
        elif item == pivot:
            same.append(item)
        elif item > pivot:
            high.append(item)

    # The final result combines the sorted `low` list
    # with the `same` list and the sorted `high` list
    return quicksort(low) + same + quicksort(high)


if __name__ == "__main__":
    # Test case 1
    arr = [3, 7, 2, 1]
    print(f'{arr} sorted: {quicksort([3, 7, 2, 1])}')
    assert quicksort([3, 7, 2, 1]) == [1, 2, 3, 7], 'Incorrectly sorted'

    # Generate an array of `ARRAY_LENGTH` items consisting
    ARRAY_LENGTH = 1000
    # Generate an array of `ARRAY_LENGTH` items consisting
    # of random integer values between 0 and 999
    array = [randint(0, 1000) for i in range(ARRAY_LENGTH)]

    # Call the function using the name of the sorting algorithm
    # and the array you just created
    run_sorting_algorithm(algorithm="quicksort", array=array)