# Copyright © 2020 way2FAANG
# LeetCode: 832


# Time: O(r*c) | Space: O(1)
def flip_and_invert_image(matrix):
    # Do it in place

    rows = len(matrix)
    cols = len(matrix[0])

    # calculate mid index
    mid = (cols - 1) // 2

    for r in range(rows):
        for c in range(mid + 1):  # careful - range is exclusive of end
            # Swap and complement in sametime - easy in pyhtone. Remember right side is evaluated first
            matrix[r][c], matrix[r][(cols - 1) - c] = matrix[r][(cols - 1) - c] ^ 1, matrix[r][c] ^ 1
    return matrix


def main():
    print(flip_and_invert_image([[1, 0, 1], [1, 1, 1], [0, 1, 1]]))
    print(flip_and_invert_image([[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]]))


main()
