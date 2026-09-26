# LeetCode: 1 - Two Sum (variation: all unique value pairs in a sorted array)

# Time: O(n) | Space: O(1) auxiliary + O(k) output for k pairs; input must be sorted
def pair_with_targetsum(arr, target_sum):
    result = []
    left, right = 0, len(arr)-1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target_sum:
            result.append([arr[left], arr[right]])
            # As we need to find all pairs summing to target_sum and not jus the first one  we will continue
            left += 1
            right -= 1
            # Handle duplicates
            # Need to check left < right in these cases
            # because while handling duplicates our left may cross right making it an invalid case
            # e.g. [2, 2, 2, 2, 1] target_sum =3
            while left < right and arr[left] == arr[left - 1]:
                left += 1
            while left < right and arr[right] == arr[right + 1]:
                right -= 1
        elif current_sum < target_sum:
            left += 1
        else:
            right -= 1
    return result


if __name__ == '__main__':

    print(pair_with_targetsum([1, 2, 2, 2, 3, 4, 4, 4, 5, 6], 6))
    print(pair_with_targetsum([2, 5, 9, 11], 11))
