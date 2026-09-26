# O(N) time | O(N) space for output
def make_squares(nums):
    sorted_squares = [0 for _ in range(len(nums))]
    # two pointers
    left, right = 0, len(nums) - 1
    # output pointer
    sorted_squares_index = len(nums) - 1
    while left <= right:
        left_square = nums[left] ** 2
        right_square = nums[right] ** 2
        if left_square > right_square:
            sorted_squares[sorted_squares_index] = left_square
            # Move pointer
            left += 1
        else:
            sorted_squares[sorted_squares_index] = right_square
            # Move pointer
            right -= 1
        sorted_squares_index -= 1
    return sorted_squares


def main():
    print("Squares: " + str(make_squares([-2, -1, 0, 2, 3])))
    print("Squares: " + str(make_squares([-3, -1, 0, 1, 2])))


main()
