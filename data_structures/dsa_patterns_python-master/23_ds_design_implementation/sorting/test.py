from random import randint


def quicksort(arr):
    # base case
    if len(arr) <= 1:
        return arr

    n = len(arr)
    pivot = arr[randint(0, n-1)]

    low, high, same = [], [], []

    for i in range(n):
        if arr[i] < pivot:
            low.append(arr[i])
        elif arr[i] == pivot:
            same.append(arr[i])
        else:
            high.append(arr[i])

    return quicksort(low) + same + quicksort(high)


if __name__ == '__main__':
    # Test case 1
    arr = [3, 7, 2, 1]
    print(f'{arr} sorted: {quicksort([3, 7, 2, 1])}')
    assert quicksort([3, 7, 2, 1]) == [1, 2, 3, 7], 'Incorrectly sorted'