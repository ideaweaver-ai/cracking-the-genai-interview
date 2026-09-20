# Copyright © 2020 way2FAANG
# LeetCode: 136


# Time: O(n) | Space: O(1) - improvement over hashmap solution
def find_single_number(arr):
    result = 0  # since any number xored with 0 is number itself - so 0^arr[0] = arr[0]
    for num in arr:
        result ^= num
    return result


def main():
    arr = [1, 4, 2, 1, 3, 2, 3]
    print(find_single_number(arr))


main()
