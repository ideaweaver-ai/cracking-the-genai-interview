# from collections import deque
#
#
# # O(n) time | O(n) space | No advantage of using deque. as converting deque to list is O(n)
# def make_squares(arr):
#     squares = deque()
#     # TODO: Write your code here
#     left, right = 0, len(arr) - 1
#     while left < right:
#         if abs(arr[left]) > abs(arr[right]):
#             squares.appendleft(arr[left] ** 2)
#             left += 1
#         else:
#             squares.appendleft(arr[right] ** 2)
#             right -= 1
#     return list(squares)


# find the first non negative number and then move two pointers in opposite direction
# O(n) time | O(1) space
# def make_squares(arr):
#     squares = []
#     first_positive_index = 0
#     while first_positive_index < len(arr):
#         if arr[first_positive_index] >= 0:
#             break
#         first_positive_index += 1
#
#     # all negatives
#     if first_positive_index == len(arr):
#         return [num ** 2 for num in arr]
#
#     left, right = first_positive_index - 1, first_positive_index
#
#     while left >= 0 or right < len(arr):
#         if right >= len(arr) or abs(arr[left]) < abs(arr[right]):
#             squares.append(arr[left] ** 2)
#             left -= 1
#         else:
#             squares.append(arr[right] ** 2)
#             right += 1
#
#     return squares

# O(N) time | O(N) space for output
def make_squares(arr):
    squares = [0 for _ in range(len(arr))]
    # two pointers
    left, right = 0, len(arr) - 1
    # output pointer
    squares_index = len(arr) - 1
    while left <= right:
        left_square = arr[left] ** 2
        right_square = arr[right] ** 2
        if left_square > right_square:
            squares[squares_index] = left_square
            # Move pointer
            left += 1
        else:
            squares[squares_index] = right_square
            # Move pointer
            right -= 1
        squares_index -= 1
    return squares


def main():
    print("Squares: " + str(make_squares([-2, -1, 0, 2, 3])))
    print("Squares: " + str(make_squares([-3, -1, 0, 1, 2])))


main()
