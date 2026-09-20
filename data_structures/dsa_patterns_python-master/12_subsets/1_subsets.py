# Copyright © 2020 way2FAANG
# LeetCode: 78

# Time: O(n * 2**n) | Space: O(1) excluding result,  O(n * 2**n) including the output list(subsets)
# we will take all existing subsets and insert the current number in them to create new subsets
def find_subsets(nums):
    # very imp in bfs
    # since we are appending to subsets list, its imp to know how many elements to track
    # *** This code will cause an infinite loop
    # for subset in subsets:
    #   new_subset = list(subset)  # create a copy of subset
    #   # add current num to the subset
    #   new_subset.append(num)
    #   subsets.append(new_subset)
    # *** because we are appending new subset the subsets list and iterating over it. This will cause infinite error

    # initialize bfs (Note: not a queue)
    subsets = list()
    subsets.append([])  # imp - start with empty set

    # main bfs loop - slightly different than normal
    # here we add num to all previous subsets in the previous level (level_size) to create new subsets
    for num in nums:
        # ** imp: level size ??
        # since we are modifying subsets in each iteration, we will be stuck in an infinite loop if we iterate over range(len(subsets))
        level_size = len(subsets)
        for subset_index in range(level_size):
            new_subset = list(subsets[subset_index])  # create a copy of current subset to create new subset
            new_subset.append(num)
            subsets.append(new_subset)
    return subsets


def main():
    print("Here is the list of subsets: " + str(find_subsets([1, 3])))
    print("Here is the list of subsets: " + str(find_subsets([1, 5, 3])))


main()
