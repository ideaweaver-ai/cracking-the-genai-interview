# Copyright © 2020 way2FAANG
# LeetCode: 260


# Time: O(n) | Space: O(1) - improvement over hash map
def find_single_numbers(nums):
    # XOR all nums - we will get xor of the two single nums
    n1xorn2 = 0
    for num in nums:
        n1xorn2 ^= num

    # since the two single nums are different, at least 1 bit should be set in the XOR
    # find right most set bit in n1xorn2 - it differentiates the two nums (1 in one num and 0 in other)
    rightmost_set_bit = 1 # in n1xorn2
    while rightmost_set_bit & n1xorn2 == 0:  # & - bitwise and, will be non zero only when we reach right most set bit
        rightmost_set_bit <<= 1

    # use the rightmost_set_bit to put all nums in array into two baskets: num1, num2
    # since all other nums are repeated twice, both the occurences will map to same basket and their XOR will be 0
    # ultimately num1 and num2, will hold the two nums that are not repeated
    num1, num2 = 0, 0
    for num in nums:
        if rightmost_set_bit & num:  # num's bit  in same position of rightmost_set_bit is set
            num1 ^= num
        else:  # num's bit  in same position of rightmost_set_bit is not set
            num2 ^= num

    return [num1, num2]


def main():
    print('Single numbers are:' +
          str(find_single_numbers([1, 4, 2, 1, 3, 5, 6, 2, 3, 5])))
    print('Single numbers are:' + str(find_single_numbers([2, 1, 3, 2])))


main()
