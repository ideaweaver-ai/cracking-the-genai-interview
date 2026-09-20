# Copyright © 2020 way2FAANG
# LeetCode: 744


# Time: O(log(n)) | Space: O(1)
def search_next_letter(letters, key):
    n = len(letters)

    if key >= letters[-1] or key < letters[0]:
        return letters[0]  # circular array

    start, end = 0, len(letters) - 1
    while start <= end:  # do you understand why equal is not there - try an example of arr sized 2
        mid = start + (end - start) // 2
        if key == letters[mid]:
            return letters[(mid + 1) % n]  # we have to return the next letter not the index

        elif key < letters[mid]:
            end = mid - 1
        else:
            start = mid + 1

    return letters[start % n]


# # little more intelligent - we dont need to cater to key == arr[mid]
# # case specially as we always have to return the next element
# def search_next_letter(letters, key):
#     n = len(letters)
#     if key < letters[0] or key > letters[n - 1]:
#         return letters[0]
#
#     start, end = 0, n - 1
#     while start <= end:
#         mid = start + (end - start) // 2
#         if key < letters[mid]:
#             end = mid - 1
#         else:  # key >= letters[mid]:
#             start = mid + 1
#
#     # since the loop is running until 'start <= end', so at the end of the while loop, 'start == end+1'
#     return letters[start % n]


def main():
    print(search_next_letter(['a', 'c', 'f', 'h'], 'f'))
    print(search_next_letter(['a', 'c', 'f', 'h'], 'b'))
    print(search_next_letter(['a', 'c', 'f', 'h'], 'm'))


main()
