# Copyright © 2020 way2FAANG
# LeetCode: 1009

# Time: O(n) | Space: O(1)


# Algo
# How to calculate complement = all_bits_set ^ number. We have to just calculate all_bits_set
# Calculate number of bits
# Calculate all_bits_set
# return complement
def calculate_bitwise_complement(n):
    num_bits = 0
    n_copy = n
    while n_copy:
        num_bits += 1
        n_copy >>= 1

    # all_bits_set = 0
    # for _ in range(num_bits):
    #     all_bits_set <<= 1
    #     all_bits_set += 1

    # another way to calculate all_bits_set
    all_bits_set = pow(2, num_bits)-1

    return all_bits_set ^ n


def main():
    print('Bitwise complement is: ' + str(calculate_bitwise_complement(8)))
    print('Bitwise complement is: ' + str(calculate_bitwise_complement(10)))


main()