# Copyright © 2020 way2FAANG
# LeetCode: 784

# Time: Total 2**n options. At each iteration we generate a new string = O(n)
# Time = O(n * 2**n)
# Space = O(n * 2**n) including the output var
def find_letter_case_string_permutations(str):
    # initialize bfs queu
    permutations = [str]
    for i in range(len(str)):
        if str[i].isnumeric():
            continue
        level_size = len(permutations)
        for j in range(level_size):
            new_permutation = permutations[j]  # string - immutable, so no need to create copy (list)
            # if the current character is in upper case, change it to lower case or vice versa
            new_permutation = new_permutation[:i] + new_permutation[i].swapcase() + new_permutation[i + 1:]
            permutations.append(new_permutation)
    return permutations


def main():
    print("String permutations are: " +
          str(find_letter_case_string_permutations("ad52")))
    print("String permutations are: " +
          str(find_letter_case_string_permutations("ab7c")))


main()
