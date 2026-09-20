# Copyright © 2020 way2FAANG
# LeetCode: 320

from collections import deque


# Time: O(n*2^n) | Space: O(n*2^n)
def generate_generalized_abbreviation(word):
    queue = deque()
    queue.append("")
    for i in range(len(word)):
        level_size = len(queue)
        for j in range(level_size):
            current_perm = queue.popleft()
            # case 1: append letter
            next_perm = current_perm + word[i]
            queue.append(next_perm)
            # case 2: append count
            if current_perm and current_perm[-1].isdigit():
                next_perm = current_perm[:-1] + str(int(current_perm[-1]) + 1)
            else:
                next_perm = current_perm + "1"
            queue.append(next_perm)
    return list(queue)


def generate_generalized_abbreviation_recursive(word):
    result = []
    helper(word, 0, "", result)
    return result


def helper(word, i, current_perm, result):
    if i == len(word):
        result.append(current_perm)
        return

    # append letter
    next_perm = current_perm + word[i]
    helper(word, i + 1, next_perm, result)
    # append count:
    if current_perm and current_perm[-1].isdigit():
        next_perm = current_perm[:-1] + str(int(current_perm[-1]) + 1)
    else:
        next_perm = current_perm + "1"
    helper(word, i + 1, next_perm, result)


# Complicated
# class AbbreviatedWord:
#     def __init__(self, str_, count):
#         self.str_ = str_
#         self.count = count  # count of ongoing abbreviations
#
#
# def add_abbreviations_to_string(abr):
#     if abr.count != 0:
#         #  add abbreviation to string only when count > 0
#         abr.str_.append(str(abr.count))
#         abr.count = 0  # reset count
#         # no need to return anything as we are modifying the object (immutable)
#


# def generate_generalized_abbreviation(word):
#     result = []
#     queue = deque()
#     queue.append(AbbreviatedWord([], 0))
#     for i in range(len(word)):
#         char = word[i]
#         n = len(queue)
#         for j in range(n):
#             current_abr = queue.popleft()
#
#             # Case 1: add abbreviation
#             new_abr = AbbreviatedWord(list(current_abr.str_), current_abr.count)  # important create
#             new_abr.count += 1
#             # if we are at last letter attach to result else add in queue
#             if i == len(word) - 1:
#                 # if we are adding to result add abbreviations to string
#                 add_abbreviations_to_string(new_abr)
#                 result.append(''.join(new_abr.str_))
#             else:
#                 queue.append(new_abr)
#
#             # Case 2 : add letter
#             new_abr = AbbreviatedWord(list(current_abr.str_), current_abr.count)
#             add_abbreviations_to_string(new_abr)
#             new_abr.str_.append(char)
#             if i == len(word) - 1:
#                 result.append(''.join(new_abr.str_))
#             else:
#                 queue.append(new_abr)
#     return result


def main():
    print("Generalized abbreviation are: " +
          str(generate_generalized_abbreviation("BAT")))
    print("Generalized abbreviation are: " +
          str(generate_generalized_abbreviation("code")))


main()
