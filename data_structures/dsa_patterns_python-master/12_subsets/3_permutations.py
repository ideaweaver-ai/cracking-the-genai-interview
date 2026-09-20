# Copyright © 2020 way2FAANG
# LeetCode: 46

from collections import deque


# To create a permutation we need to insert the num at every index in old permutation,
# not just append it as in finding subsets. Rest of the code is same
# Time: n! total permutations. To generate permutations we insert index at each element O(n)
# So total time: O(n*n!)
# Space: Queue space - Max n! items in queue, each having n elements = O(n*n!)
def find_permutations(nums):
    permutations = []

    # initialize bfs queue
    queue = deque()
    # why deque ? - because all lists (permutations) having len < len of nums are not permutations
    # they are just helping us to create the actual permutation
    queue.append([])

    # bfs loop
    for num in nums:
        # level size
        lelvel_size = len(queue)

        for _ in range(lelvel_size):
            # we used deque because we don't need the old permutation in the bfs queue unlike subsets
            # and deleting in a list is O(n). instead deque popleft is O(1)
            old_permutation = queue.popleft()
            for j in range(len(old_permutation) + 1):
                # difference compared to subsets problem, instead of append we need to insert num at every index
                new_permutation = list(old_permutation)  # create a copy for every new permutation to be created
                new_permutation.insert(j, num)
                if len(new_permutation) == len(nums):
                    permutations.append(new_permutation)
                else:
                    queue.append(new_permutation)
    return permutations


def main():
    print("Here are all the permutations: " + str(find_permutations([1, 3, 5])))


main()
