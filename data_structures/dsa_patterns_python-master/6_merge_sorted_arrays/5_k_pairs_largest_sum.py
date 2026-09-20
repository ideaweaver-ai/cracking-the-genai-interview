# Copyright © 2020 way2FAANG
# LeetCode: 373

from heapq import heappush, heappop


# Time: O(n*m*log(k)) - if we assume at least k elements in each array it is O(k^2log(k))
# Space: O(k)
def find_k_largest_pairs(nums1, nums2, k):
    # Top k pattern - so we will use min heap
    min_heap = []
    # to find the k largest elements, we need max k elements from arr1 and k from arr2
    for i in range(min(k, len(nums1))):
        for j in range(min(k, len(nums2))):
            if len(min_heap) < k:
                heappush(min_heap, (nums1[i] + nums2[j], nums1[i], nums2[j]))
            else:
                # if the sum of the two numbers from the two arrays is smaller than the smallest(top)
                # element of the heap, we can 'break' here. Since the arrays are sorted in the
                # descending order, we'll not be able to find a pair with a higher sum moving forward
                if nums1[i] + nums2[j] < min_heap[0][0]:
                    break
                else:
                    heappop(min_heap)
                    heappush(min_heap, (nums1[i] + nums2[j], nums1[i], nums2[j]))

    # Output
    result = []
    for sum_, num1, num2 in min_heap:
        result.append([num1, num2])
    return result


# Better solution
# Time: O(min(n,m) * log(k)) - if we assume at least k elements in each array it is O(klog(k))
# Space: O(k)
def find_k_largest_pairs(nums1, nums2, k):
    max_heap = []
    result = []
    # add the first element
    heappush(max_heap, (-(nums1[0] + nums2[0]), 0, 0))
    while len(result) < k and max_heap:
        num, index1, index2 = heappop(max_heap)
        result.append([nums1[index1], nums2[index2]])

        if index2 + 1 < len(nums2):
            heappush(max_heap, (-(nums1[index1] + nums2[index2 + 1]), index1, index2 + 1))

        if index1 + 1 < len(nums1):
            heappush(max_heap, (-(nums1[index1 + 1] + nums2[index2]), index1 + 1, index2))

    return result


def main():
    print("Pairs with largest sum are: " +
          str(find_k_largest_pairs([9, 8, 2], [6, 3, 1], 3)))


main()
