# Two Pointers

Study order reflects the requested reordering; difficulty labels follow the supplied table.

## Practice

| # | LeetCode | Problem | Difficulty | Local solution |
| --: | --: | --- | --- | --- |
| 1 | 1 | Two Sum | easy | [1_1_pair_with_target_sum.py](1_1_pair_with_target_sum.py) |
| 2 | 26 | Remove Duplicates | easy | [2_1_remove_duplicates.py](2_1_remove_duplicates.py) |
| 3 | 977 | Squaring a Sorted Array | easy | [3_square_sorted_array.py](3_square_sorted_array.py) |
| 4 | 75 | Dutch National Flag Problem | medium | [4_dutch_flag.py](4_dutch_flag.py) |
| 5 | 15 | Triplet Sum to Zero | medium | [5_three_pair_sum.py](5_three_pair_sum.py) |
| 6 | 16 | Triplet Sum Close to Target | medium | [6_triplet_sum_close_to_target.py](6_triplet_sum_close_to_target.py) |
| 7 | 259 | Triplets with Smaller Sum | medium | [7_triplets_with_smaller_sum.py](7_triplets_with_smaller_sum.py) |
| 8 | 186 | Reverse Words in a String II | medium | [8_reverse_words_in_a_string_ii.py](8_reverse_words_in_a_string_ii.py) |

## Homework

| # | LeetCode | Problem | Difficulty | Local solution |
| --: | --: | --- | --- | --- |
| 9 | 27 | Remove all instances of a key | easy | [9_remove_all_instances_of_key_in_place.py](9_remove_all_instances_of_key_in_place.py) |
| 10 | 581 | Minimum Subarray to Sort | medium | [10_min_subarray_to_sort.py](10_min_subarray_to_sort.py) |
| 11 | 18 | Quadruple Sum to Target | hard | [11_pc1_quadruplets_sum.py](11_pc1_quadruplets_sum.py) |
| 12 | 713 | Subarrays with Product Less than a Target — solve LeetCode also, slight variation | medium | [12_subarrays_with_prod_less_than_target.py](12_subarrays_with_prod_less_than_target.py) |

## Hard

| # | LeetCode | Problem | Difficulty | Local solution |
| --: | --: | --- | --- | --- |
| 13 | 844 | Comparing Strings containing Backspaces | easy | [13_pc2_comparing_strings_with_backspaces.py](13_pc2_comparing_strings_with_backspaces.py) |
| 14 | 42 | Maximum Trapping Water | hard | Not present in this folder |

## Variants and additional problems

- [All unique pairs](1_2_generic_pair_with_target_sum.py): Two Sum variant requiring sorted input.
- [Return triplets with smaller sum](7_2_triplets_with_smaller_sum.py): returns triplets; LeetCode 259 asks for the count.
- [Count subarrays with product less than k](12_2_count_subarrays_with_prod_less_than_k.py): the counting version for LeetCode 713.
- [Container With Most Water](12_container_with_most_water.py): LeetCode 11; a different problem from Trapping Rain Water (42).
- [Next Permutation](13_next_permutation.py): LeetCode 31.
- [First Come, First Served](14_first_come_first_serve.py): Interview Cake problem; no direct LeetCode mapping assigned.

## Complexity notation

Comments above solution and helper functions describe their implementations. `n` is the input length unless stated otherwise; `k` is the number of returned items. Python sorting can require O(n) auxiliary memory. Output storage is listed separately where relevant. Demo entry points and unit tests are not algorithm complexity annotations.
