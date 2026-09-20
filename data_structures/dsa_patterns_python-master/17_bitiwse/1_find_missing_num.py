# Copyright © 2020 way2FAANG
# LeetCode: 268

# Given an array of n-1n−1 integers in the range from 11 to nn, find the one number that is missing from the array.


# Time: O(n) | Space: O(1)
def find_missing_number(arr):
    n = len(arr) + 1
    # find sum of all numbers from 1 to n.
    s1 = 0
    for i in range(1, n + 1):
        s1 += i

    # subtract all numbers in input from sum.
    for i in arr:
        s1 -= i

    # s1, now, is the missing number
    return s1
# Problem with above approach: Integer overflow


def find_missing_number(arr):
    n = len(arr) + 1
    # XOR of all values from 1 to n
    x1 = 1
    for i in range(2, n + 1):
        x1 ^= i

    # XOR of all values in arr
    x2 = arr[0]
    for i in range(1, n - 1):
        x2 = x2 ^ arr[i]

    # missing number is the xor of x1 and x2
    # why - XOR is associative and commutative - hence we can rearrange x1 ^ x2
    # x1^x2 = each number will xor with itself (XOR to 0) except missing number
    # x1^x2 = 0 ^ missing_num = missing_num , since any number XORed with 0 is itself
    return x1 ^ x2


def main():
    arr = [1, 5, 2, 6, 4]
    print('Missing number is:' + str(find_missing_number(arr)))


main()
