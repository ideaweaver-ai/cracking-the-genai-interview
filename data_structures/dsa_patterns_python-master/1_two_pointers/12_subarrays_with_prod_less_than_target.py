# LeetCode: 713 - Subarray Product Less Than K (variation: return subarrays instead of their count)

from collections import deque
# Brute force
# def find_subarrays(arr, target):
#     result = []
#     # TODO: Write your code here
#     for i in range(len(arr)):
#         current_prod = 1
#         current_list = []
#         for j in range(i, len(arr)):
#             current_prod *= arr[j]
#             current_list.append(arr[j])
#             if current_prod < target:
#                 result.append(current_list.copy()) ## vv imp. Understand why copy
#     return result


from collections import deque


# Time: O(n^3) worst case | Space: O(n) auxiliary + O(n^3) output (copied subarray elements)
def find_subarrays(arr, target):
    # Output variable
    result = []
    # Define window start and metric
    start, product = 0, 1

    # Slide window
    for end in range(len(arr)):
        # Expand
        product *= arr[end]
        # Validate window
        while product >= target and start < end:  # imp to check start < end
            product /= arr[start]
            start += 1
        # Window valid
        # How do we consider all the subarrays in the valid window
        # if we iterate from start to end and consider all subarrays we will have duplicates
        # e.g. valid window = [2,5] we will append [2] twon times, once when end is 2 and next when end is 5
        # hence we go backwards and consider every subarray from end to start, this way we dont have duplicates
        sub_array = deque()
        for k in range(end, start - 1, -1):
            sub_array.appendleft(arr[k])
            result.append(list(sub_array))
    return result


def main():
    print(find_subarrays([2, 5, 3, 10], 30))
    print(find_subarrays([8, 2, 6, 5], 50))


main()
