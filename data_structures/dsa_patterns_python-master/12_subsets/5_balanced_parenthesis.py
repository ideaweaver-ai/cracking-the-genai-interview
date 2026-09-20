# Copyright © 2020 way2FAANG
# LeetCode: 22

from collections import deque


class Parenthesis:
    def __init__(self, str_, open_, closed):
        self.str_ = str_
        self.open_ = open_
        self.closed = closed


# Time: If we ignore '(' should come before ')', worst case we will have 2^N possible permutations.
# When creating a new permutation we are adding '(' or ')' to a string. Since string is immutable this O(N)
# So total time: O(N*2^N)
# Can using a list instead of string improve TC ?
# On the surface it looks likely, but look closely
# In each iteration, we don't want to modify current. So we create a new object of Parenthesis
# So even if we use list the list will need to be copied as we don't need the same list to be referenced at two Parenthesis objects

# Space: O(N*2^N) including the output
def generate_valid_parentheses(num):
    result = []
    queue = deque()
    queue.append(Parenthesis('', 0, 0))
    while queue:
        # since we are popping, queue will reduce overtime and while loop will terminate
        current_parenthesis = queue.popleft()
        # check if we have an output
        if current_parenthesis.open_ == num and current_parenthesis.closed == num:
            result.append(current_parenthesis.str_)

        else:
            # if count of open parenthesis is < N I can append '('
            if current_parenthesis.open_ < num:
                # Don't modify current in place, we need it to check if we can add closed parenthesis
                queue.append(Parenthesis(current_parenthesis.str_ + '(', current_parenthesis.open_ + 1, current_parenthesis.closed))
            # We can add a closed  parenthesis only if we have enough open parenthesis
            if current_parenthesis.closed < current_parenthesis.open_:
                queue.append(Parenthesis(current_parenthesis.str_ + ')', current_parenthesis.open_, current_parenthesis.closed + 1))
    return result


# Recursive
def generate_valid_parentheses(num):
    result = []
    generate_valid_parentheses_helper('', 0, 0, result, num)
    return result


def generate_valid_parentheses_helper(str_, open_, closed, result, num):
    # inner function, No need to pass num,result from outer function.
    # Be careful, don't shadow variable names
    if open_ == num and closed == num:
        result.append(str_)
        return
    else:
        # recursive calls
        if open_ < num:
            generate_valid_parentheses_helper(str_ + '(', open_ + 1, closed)

        if closed < open_:
            generate_valid_parentheses_helper(str_ + ')', open_, closed + 1)

    # no need to return anything as result is being modified in place


def main():
    print("All combinations of balanced parentheses are: " +
          str(generate_valid_parentheses(2)))
    print("All combinations of balanced parentheses are: " +
          str(generate_valid_parentheses(3)))


main()
