# LeetCode: 18 - 4Sum

# Same as triplets
# Time: O(n^3) | Space: O(n) sorting + O(k) output; k = number of quadruplets
def search_quadruplets(arr, target):
    # O/p var
    quadruplets = []
    # Don't forget to sort the array
    arr.sort()
    for i in range(len(arr) - 3):
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        for j in range(i + 1, len(arr) - 2):
            if j > i + 1 and arr[j] == arr[j - 1]:
                continue
            pair1_sum = arr[i] + arr[j]
            search_pairs(arr, target - pair1_sum, i, j, quadruplets)
    return quadruplets


# Time: O(n) | Space: O(1) auxiliary + O(k) appended output
def search_pairs(arr, target, i, j, quadruplets):
    left, right = j + 1, len(arr) - 1
    while left < right:
        pair_sum = arr[left] + arr[right]
        if pair_sum == target:
            quadruplets.append([arr[i], arr[j], arr[left], arr[right]])
            # imp - change bot pointers, as we want unique quadruplets
            left += 1
            right -= 1
            # handle duplicates
            while arr[left] == arr[left - 1] and left < right:
                left += 1
            while arr[right] == arr[right + 1] and left < right:
                right -= 1
        elif pair_sum > target:
            right -= 1
        else:
            left += 1


# without using a separate function for search_pairs. Code becomes a little simpler
# Time: O(n^3) | Space: O(n) sorting + O(k) output; k = number of quadruplets
def search_quadruplets(arr, target):
    # O/p var
    quadruplets = []

    # Don't forget to sort the array
    arr.sort()
    for i in range(len(arr) - 3):
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        for j in range(i + i, len(arr) - 2):
            if arr[j] == arr[j - 1]:
                continue
            left, right = j + 1, len(arr) - 1
            while left < right:
                current_sum = arr[i] + arr[j] + arr[left] + arr[right]
                if current_sum == target:
                    quadruplets.append([arr[i], arr[j], arr[left], arr[right]])
                    # imp - change bot pointers, as we want unique quadruplets
                    left += 1
                    right -= 1
                    # handle duplicates
                    while left < right and arr[left] == arr[left] - 1:
                        left += 1
                    while left < right and arr[right] == arr[right] + 1:
                        right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1


# Time: O(n^2 + k), O(n^4) worst case | Space: O(n^2) hash map + O(k) output
def search_quadruplets(arr, target):
  quadruplets = []
  pair_sum_map = {}

  for i in range(len(arr)-1):
    # check for pairs with complimentary sum
    for j in range(i+1, len(arr)):
      current_sum = arr[i]+arr[j]
      req_sum = target - current_sum
      if req_sum in pair_sum_map:
        for pair in pair_sum_map.get(req_sum):
          num1, num2 = pair
          quadruplets.append([num1, num2, arr[i], arr[j]]) # since arr is sorted don't need sorting here
    # add pair to pair sum
    for k in range(i):
      n1_n2_sum = arr[k]+arr[i]
      if n1_n2_sum in pair_sum_map:
        pair_sum_map.get(n1_n2_sum).append([arr[k], arr[i]])
      else:
        pair_sum_map[n1_n2_sum] = [[arr[k], arr[i]]]
  return quadruplets # to make unique we need to make quadruplets a set and convert it back to lidt - O(n**4) step


def main():
    print(search_quadruplets([4, 1, 2, -1, 1, -3], 1))
    print(search_quadruplets([2, 0, -1, 1, -2, 2], 2))


main()
