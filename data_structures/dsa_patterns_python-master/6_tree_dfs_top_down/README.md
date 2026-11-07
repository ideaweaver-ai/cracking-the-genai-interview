# Tree DFS: top-down

Pass information about ancestors to children through DFS arguments: a path slate, remaining sum, bounds, or depth. Shared result lists collect answers. Problem 0 uses BFS for comparison; problem 1 uses DFS. Both print every root-to-leaf path, one per line, and also expose `find_paths` for returning the paths.

## Code style

Based on *Trees Practice Session 2*: handle an empty root in the public function, use a nested `dfs(node, ...)`, and call it only on existing children. Distinguish leaf cases when they require special work. Mutable path slates use append/pop backtracking; copy a slate when saving a path. Shared scalar answers use one-element lists scoped to each call.

Examples run only under the `__main__` guard. Each problem is self-contained with its own node class. In complexity notes, `n` is the node count, `h` the tree height, and `w` the maximum width. Output storage is separate from auxiliary space.

## Problems

- [0 all root to leaf paths bfs](0_all_root_to_leaf_paths_bfs.py)
- [1 all root to leaf paths](1_all_root_to_leaf_paths.py)
- [2 path sum](2_path_sum.py)
- [3 all paths for sum](3_all_paths_for_sum.py)
- [4 longest consecutive sequence](4_longest_consecutive_sequence.py)
- [5 count paths for sum](5_count_paths_for_sum.py)
- [6 invert binary tree](6_invert_binary_tree.py)
- [7 nary tree height](7_nary_tree_height.py)
- [8 sum of path nums](8_sum_of_path_nums.py)
- [9 root to leaf path with max sum](9_root_to_leaf_path_with_max_sum.py)
- [10 path with given sequence](10_path_with_given_sequence.py)
- [11 return list of all nodes](11_return_list_of_all_nodes.py)
- [12 tree boundary](12_tree_boundary.py)
- [13 is valid bst](13_is_valid_bst.py)
- [14 bottom left tree value](14_bottom_left_tree_value.py)
- [15 vertical order traversal](15_vertical_order_traversal.py)
- [16 vertical traversal](16_vertical_traversal.py)
- [17 binary tree upside down](17_binary_tree_upside_down.py)
- [18 same tree](18_same_tree.py)
- [19 symmetric tree](19_symmetric_tree.py)
- [20 connect next right pointers](20_connect_next_right_pointers.py)
- [21 connect next right pointers ii](21_connect_next_right_pointers_ii.py)
- [22 clone binary tree](22_clone_binary_tree.py)
- [23 merge two binary trees](23_merge_two_binary_trees.py)

## Organization notes

The original `6_tree_dfs` collection is split between these two sibling folders. All original problem topics are retained; redundant helper variants have been consolidated. BST validation has both top-down bounds and bottom-up subtree-summary versions. N-ary height is included in both patterns for comparison.

Diameter, longest univalue path, and `find_height` count **edges**; `max_depth` counts **nodes**. The original diameter counted nodes. Empty-tree conventions are documented in each problem. The maximum root-to-leaf path returns `(sum, path)` with a flat path list. Boundary traversal returns nodes in anticlockwise order, with no duplicates.

## Session 3 coverage

All 19 distinct problems in *Trees Practice Session 3*, including its appendix, are covered across the two DFS folders. Repeated problems reuse existing implementations. Pages 4-17 introduce traversal templates; preorder traversal is in top-down problem 11, and level-order traversal remains in the BFS pattern folder. BFS alternatives shown in the slides are represented here by their DFS solutions.

| PDF pages | Problem | Implementation |
| --- | --- | --- |
| 18-20 | Find Bottom Left Tree Value | [Top-down 14](14_bottom_left_tree_value.py) |
| 21-25 | Binary Tree Vertical Order Traversal (314) | [Top-down 15](15_vertical_order_traversal.py) |
| 26-28 | Vertical Order Traversal (987) | [Top-down 16](16_vertical_traversal.py) |
| 29-32 | Boundary of Binary Tree | [Top-down 12](12_tree_boundary.py) |
| 33-35 | Binary Tree Upside Down | [Top-down 17](17_binary_tree_upside_down.py) |
| 37-39 | Balanced Binary Tree | [Bottom-up 8](../7_tree_dfs_bottom_up/8_balanced_binary_tree.py) |
| 40-43 | Validate Binary Search Tree | [Bottom-up 5](../7_tree_dfs_bottom_up/5_is_valid_bst.py) |
| 44-46 | Largest BST Subtree | [Bottom-up 9](../7_tree_dfs_bottom_up/9_largest_bst_subtree.py) |
| 47-48 | Longest Univalue Path | [Bottom-up 6](../7_tree_dfs_bottom_up/6_longest_univalue_path.py) |
| 49-50 | Binary Tree Maximum Path Sum | [Bottom-up 7](../7_tree_dfs_bottom_up/7_path_with_max_sum.py) |
| 52-53 | Same Tree | [Top-down 18](18_same_tree.py) |
| 54-55 | Symmetric Tree | [Top-down 19](19_symmetric_tree.py) |
| 56-57 | Populating Next Right Pointers (perfect tree) | [Top-down 20](20_connect_next_right_pointers.py) |
| 58-60 | Populating Next Right Pointers II (general tree) | [Top-down 21](21_connect_next_right_pointers_ii.py) |
| 61-62 | Clone a Binary Tree | [Top-down 22](22_clone_binary_tree.py) |
| 63-65 | Merge Two Binary Trees | [Top-down 23](23_merge_two_binary_trees.py) |
| 68-69 | Diameter of Binary Tree | [Bottom-up 2](../7_tree_dfs_bottom_up/2_tree_diameter.py) |
| 70-72 | Count Univalue Subtrees | [Bottom-up 3](../7_tree_dfs_bottom_up/3_count_univalue_subtrees.py) |
| 73-74 | Lowest Common Ancestor | [Bottom-up 4](../7_tree_dfs_bottom_up/4_lowest_common_ancestor.py) |

Problems 314 and 987 have different tie rules: 314 keeps left-to-right order, while 987 sorts equal-position values. Upside-down conversion assumes every right child is a leaf with a left sibling. Next-pointer problem 116 assumes a perfect tree; 117 handles sparse trees and visits right children first. Cloning creates independent nodes; merging mutates the first tree and reuses unmatched branches of the second.
