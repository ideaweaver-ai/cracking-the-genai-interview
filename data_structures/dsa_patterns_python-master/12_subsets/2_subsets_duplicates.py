# Copyright © 2020 way2FAANG
# LeetCode: 90


# Time: O(n * 2**n) | Space: O(1) excluding result,  O(n * 2**n) including the output list(subsets)
def find_subsets(nums):
    # ** imp sort sums so duplicates are together
    nums.sort()

    # initialize bfs
    subsets = [[]]  # imp - start with empty set

    # main bfs
    for i in range(len(nums)):
        start_index = 0
        # whenever there is a duplicate, create subsets only from the subsets added in previous iteration
        if i > 0 and nums[i] == nums[i - 1]:
            start_index = level_size

        # level size
        level_size = len(subsets)
        for subset_index in range(start_index, level_size):
            new_subset = list(subsets[subset_index])
            new_subset.append(nums[i])
            subsets.append(new_subset)
    return subsets


def main():
    print("Here is the list of subsets: " + str(find_subsets([1, 3, 3])))
    print("Here is the list of subsets: " + str(find_subsets([1, 5, 3, 3])))


main()
