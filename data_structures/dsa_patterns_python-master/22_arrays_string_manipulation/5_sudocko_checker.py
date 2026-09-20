# Copyright © 2020 way2FAANG
# LeetCode: 36

import math
from typing import List


# simple iterative solution
# Time: O(n**2) | Space: O(n**2)
# Time: O(1) | Space: O(1)
class Solution:
    def isValidSudoku(self, board):
        # init data
        rows = [{} for i in range(9)]
        columns = [{} for i in range(9)]
        boxes = [{} for i in range(9)]

        # validate a board
        for i in range(9):
            for j in range(9):
                num = board[i][j]
                if num != '.':
                    num = int(num)
                    box_index = (i // 3) * 3 + j // 3

                    # keep the current cell value
                    rows[i][num] = rows[i].get(num, 0) + 1
                    columns[j][num] = columns[j].get(num, 0) + 1
                    boxes[box_index][num] = boxes[box_index].get(num, 0) + 1

                    # check if this value has been already seen before
                    if rows[i][num] > 1 or columns[j][num] > 1 or boxes[box_index][num] > 1:
                        return False
        return True


# class Solution:
#     def isValidSudoku(self, board: List[List[str]]) -> bool:
#         def has_duplicate(block: List[str]):
#             block = list(filter(lambda x: x != ".", block))
#             type(block)
#             return len(block) != len(set(block))
#
#         # main function
#         n = len(board)
#         does_row_contain_duplicate = [has_duplicate(board[i]) for i in range(n)]
#         does_col_contain_duplicate = [has_duplicate([board[i][j] for i in range(n)]) for j in range(n)]
#         # print(does_row_contain_duplicate)
#         # print(does_col_contain_duplicate)
#         if any(does_row_contain_duplicate) or any(does_col_contain_duplicate):
#             return False
#
#         # block wise check
#         block_size = int(math.sqrt(n))
#
#         if any(has_duplicate([board[a][b]
#                               for a in range(block_size * I, block_size * (I + 1))
#                               for b in range(block_size * J, block_size * (J + 1))])
#                for I in range(block_size) for J in range(block_size)):
#             return False
#         return True


if __name__ == "__main__":
    sol = Solution()
    board = [["5", "3", ".", ".", "7", ".", ".", ".", "."]
        , ["6", ".", ".", "1", "9", "5", ".", ".", "."]
        , [".", "9", "8", ".", ".", ".", ".", "6", "."]
        , ["8", ".", ".", ".", "6", ".", ".", ".", "3"]
        , ["4", ".", ".", "8", ".", "3", ".", ".", "1"]
        , ["7", ".", ".", ".", "2", ".", ".", ".", "6"]
        , [".", "6", ".", ".", ".", ".", "2", "8", "."]
        , [".", ".", ".", "4", "1", "9", ".", ".", "5"]
        , [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

    assert sol.isValidSudoku(board) is True, "Test case 1 failed"
    board = [["8", "3", ".", ".", "7", ".", ".", ".", "."]
        , ["6", ".", ".", "1", "9", "5", ".", ".", "."]
        , [".", "9", "8", ".", ".", ".", ".", "6", "."]
        , ["8", ".", ".", ".", "6", ".", ".", ".", "3"]
        , ["4", ".", ".", "8", ".", "3", ".", ".", "1"]
        , ["7", ".", ".", ".", "2", ".", ".", ".", "6"]
        , [".", "6", ".", ".", ".", ".", "2", "8", "."]
        , [".", ".", ".", "4", "1", "9", ".", ".", "5"]
        , [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
    assert sol.isValidSudoku(board) is False, "Test case 2 failed"
