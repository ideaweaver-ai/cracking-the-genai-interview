# LeetCode: 27 - Remove Element

# Time: O(n) | Space: O(1)
def remove_element(arr, key):
    next_non_key_index = 0
    for i in range(len(arr)):
        if arr[i] != key:
            arr[next_non_key_index] = arr[i]
            next_non_key_index += 1
    return next_non_key_index


def main():
    print("Array new length: " +
          str(remove_element([3, 2, 3, 6, 3, 10, 9, 3], 3)))
    print("Array new length: " +
          str(remove_element([2, 11, 2, 2, 1], 2)))


main()
