

# Algo
# When we are asked to find any sum, triplets, quadruplets, five_number_sum etc
# 1. sort array if not sorted
# 2. write generic pair_sum function that can find multiple pairs adding to target sum and handle duplicates
# 3. Number of for loops required in main function = m - 2 i.e. triplets = 3-2, quadruplets = 4-2, five_num_sum = 5-2
# These for loops will cover all unique combinations for remaining  numbers (for target sum) in the array
# 4. Call pair_sum in each for loop
# 5. Compared to brute force this algo will reduce time complexity by one order

# Time: O(n**2) | Space: O(n) for sorting
def search_triplets(arr):
    def pair_sum(left, right, target_sum):
        # we write this as inner function so that we don't have to pass arr, i and triplets to this func
        # if we write it as a separate func we will have to pass these parameters also
        # we can do this because, arr, i, triplets are not specific to this function call
        while left < right:
            current_sum = arr[left] + arr[right]
            if current_sum == target_sum:
                triplets.append([arr[i], arr[left], arr[right]])
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
        # No need to return anything as triplets(result) is mutable and we are updating

    # Main function
    # Sort the array as it is unsorted
    arr.sort()
    triplets = []

    for i in range(len(arr)-2):
        # check duplicates here too
        if i > 0 and arr[i] == arr[i] - 1:
            continue
        pair_sum(i + 1, len(arr) - 1, -arr[i])

    return triplets


# Another way to write the code - same algo. But above approach is more generic and preferred
# Time: O(n**2) + O(n * log(n)) = O(n**2)| O(N) space - for sorting
def search_triplets(arr):
    triplets = []
    n = len(arr)
    arr.sort()
    for i in range(len(arr)-2):
        if i > 0 and arr[i] == arr[i - 1]:  # unique pairs - imp check
            continue
        left, right = i + 1, n - 1
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            if current_sum == 0:
                triplets.append([arr[i], arr[left], arr[right]])
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
            elif current_sum > 0:
                right -= 1
            else:
                left += 1
    return triplets


if __name__ == '__main__':
    print(search_triplets([-3, 0, 1, 2, -1, 1, -2]))
    print(search_triplets([-5, 2, -1, -2, 3]))
