# Copyright © 2020 way2FAANG
# LeetCode: 990

from typing import List


class Solution:
    # Union find by rank
    # All equal vars should form a connected component
    # Then go over inequality clauses - if you find two nodes from a connected component - return false
    # else return True

    # Time: O(e*log(o)) | Space: O(o)
    # e - num of equations, o - num of operands (total e.g a, b etc.)
    def equationsPossible(self, equations: List[str]) -> bool:
        # Time: O(log(o)) | Space: O(o)
        def find(i):
            parent.setdefault(i, i)
            rank.setdefault(i, 0)
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        # Time: O(log(o)) | Space: O(o)
        def union(x, y):
            xset = find(x)
            yset = find(y)

            if xset != yset:
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:
                    parent[yset] = xset
                    rank[xset] += 1

        def split_eq(eq):
            operand1 = eq[0]
            operand2 = eq[-1]
            sign = eq[1:3]
            return operand1, operand2, sign

        # main function
        # parent and rank - dicts as we don't know how many nodes at the start
        parent = {}
        rank = {}

        # list of non equal eqs
        not_equal = []
        for equation in equations:
            operand1, operand2, sign = split_eq(equation)
            if sign == '==':
                union(operand1, operand2)
            else:
                not_equal.append([operand1, operand2])

        # Go over not equal eqs and flag if they are found in connected component
        for op1, op2 in not_equal:
            op1set = find(op1)
            op2set = find(op2)

            if op1set == op2set:
                return False

        return True


if __name__ == '__main__':
    input_ = ["a==b", "b==c", "a==c"]
    sol = Solution()
    print(f'Input: {input_} -> {sol.equationsPossible(input_)}')
    assert sol.equationsPossible(input_) is True, f" Test case 1: {input_} failed"

    input_ = ["a==b", "b!=c", "c==a"]
    sol = Solution()
    print(f'Input: {input_} -> {sol.equationsPossible(input_)}')
    assert sol.equationsPossible(input_) is False, f" Test case 1: {input_} failed"
