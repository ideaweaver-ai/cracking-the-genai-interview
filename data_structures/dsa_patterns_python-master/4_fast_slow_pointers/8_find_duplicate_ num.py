# Copyright © 2020 way2FAANG
# LeetCode: 287


from typing import List


class Solution:
    # It's mentioned not to use sort - else we could have used cyclic sort since range of nos is fixed
    # Using Floyd's algo
    # What is a cycle:
    # 1. start from index 0
    # 2. At any index i, next element in sequence is element at index arr[i]
    # 3. if there was no duplicate, then there would be n+1 in arr (sincee nos are range bound starting from 1).
    # In that case we would have exited the array (LL) when we reach the lement n+1. since arr does not have index n+1. e.g. [1, 2, 3, 4]
    # 4. since the array cannot contain n+1 and it has n+1, at least 1 um should be duplicate.
    # If continue with our algo we will be stuck in cycle and start of cycle is the duplicate num. check [1, 2, 3, 2], [1, 2, 2, 3], [2, 2, 3, 1]
    # 5. So problem reduces to finding start of the cycle

    # Time: O(n) | Space: O(1)
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0

        while True:
            # since we know there is a cycle
            slow = nums[slow]  # imp - go to the index pointed by current element
            fast = nums[nums[fast]]

            if slow == fast:
                # cycle found
                break

        # find start of cycle
        head = 0
        # cycle is formed by the actual array element not indeices
        while head != slow:
            # head and slow are still index pointers
            head = nums[head]
            slow = nums[slow]

        return head  # or slow both meet at the start of the pointer


if __name__ == '__main__':
    sol = Solution()

    # Test Case 1
    nums = [1, 3, 4, 2, 2]
    print(f'duplicate in {nums}: {sol.findDuplicate(nums)}')
    assert sol.findDuplicate(nums) == 2, " Test case 1 failed"

    # Test Case 2
    nums = [3, 1, 3, 4, 2]
    print(f'duplicate in {nums}: {sol.findDuplicate(nums)}')
    assert sol.findDuplicate(nums) == 3, " Test case 2 failed"
