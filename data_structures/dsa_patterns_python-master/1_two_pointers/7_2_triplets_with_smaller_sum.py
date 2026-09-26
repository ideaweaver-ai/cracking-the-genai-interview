# LeetCode: 259 - 3Sum Smaller (variation: return triplets instead of their count)

# Time: O(n^2 + k), O(n^3) worst case | Space: O(n) sorting + O(k) output
def triplet_with_smaller_sum(arr, target):
    arr.sort()
    triplets = []
    for i in range(len(arr) - 2):
        left, right = i + 1, len(arr) - 1
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            if current_sum < target:
                for temp in range(left + 1, right + 1):
                    triplets.append([arr[i], arr[left], arr[temp]])
                left += 1
            else:
                right -= 1
    return triplets


def main():
    print(triplet_with_smaller_sum([-1, 0, 2, 3], 3))
    print(triplet_with_smaller_sum([-1, 4, 2, 1, 3], 5))


main()
