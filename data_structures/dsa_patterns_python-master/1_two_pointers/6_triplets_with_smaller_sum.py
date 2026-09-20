# # O(N^3) time | O(1) space
# def triplet_with_smaller_sum(arr, target):
#     count = 0
#     for i in range(len(arr) - 2):
#         for j in range(i + 1, len(arr) - 1):
#             for k in range(j + 1, len(arr)):
#                 if arr[i] + arr[j] + arr[k] < target:
#                     count += 1
#     return count


# O(n**2) time | O(n) space for sorting
def triplet_with_smaller_sum(arr, target):
    count = 0
    arr.sort()
    for i in range(len(arr) - 2):
        left, right = i + 1, len(arr) - 1
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            if current_sum < target:
                # key insight
                # now all pairs where right is less than current right, with same left must have sum less than targe
                count += right - left
                # increment left to see if it can give more triplets
                # no need to reset right tp len(arr)-1 because previous value of right did not give a triplet with left
                # since arr is sorted left+1 cannot give a triplet with previous value of right
                left += 1
            else:
                # we need to reduce right to get as smaller current_sum
                right -= 1
    return count


def main():
    print(triplet_with_smaller_sum([-1, 0, 2, 3], 3))
    print(triplet_with_smaller_sum([-1, 4, 2, 1, 3], 5))


main()
