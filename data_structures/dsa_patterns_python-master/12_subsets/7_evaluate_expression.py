# Copyright © 2020 way2FAANG
# LeetCode: 241


# Time: O(n * 2**n) | Space: O(2**n)
def diff_ways_to_evaluate_expression(input):
    result = []

    # base case
    if input.isdigit():
        result.append(int(input))
    # Processing input and recursive calls
    else:
        for i in range(len(input)):
            if not input[i].isdigit():
                current_operator = input[i]

                left_result = diff_ways_to_evaluate_expression(input[:i])  # left_subexpression = input[:i]
                right_result = diff_ways_to_evaluate_expression(input[i + 1:])  # right_subexpression = input[i+1:]
                for left_operand in left_result:
                    for right_operand in right_result:
                        # result_val = eval(str(left_operand) + input[i] + str(right_operand))
                        # Or this way
                        if current_operator == '+':
                            result_val = left_operand + right_operand
                        elif current_operator == '*':
                            result_val = left_operand * right_operand
                        elif current_operator == '-':
                            result_val = left_operand - right_operand
                        result.append(result_val)
    return result


# Memoized version
# Avoids duplicate calculation of same input, but does not improve TC & SC
# def diff_ways_to_evaluate_expression(input, memo={}):
#     # check in memo
#     if input in memo:
#         return memo[input]
#
#     result = []
#
#     # base case
#     if input.isdigit():
#         result.append(int(input))
#     # Processing input and recursive calls
#     else:
#         for i in range(len(input)):
#             if not input[i].isdigit():
#                 current_operator = input[i]
#
#                 left_result = diff_ways_to_evaluate_expression(input[:i])  # left_subexpression = input[:i]
#                 right_result = diff_ways_to_evaluate_expression(input[i + 1:])  # right_subexpression = input[i+1:]
#                 for left_operand in left_result:
#                     for right_operand in right_result:
#                         # result_val = eval(str(left_operand) + input[i] + str(right_operand))
#                         # Or this way
#                         if current_operator == '+':
#                             result_val = left_operand + right_operand
#                         elif current_operator == '*':
#                             result_val = left_operand * right_operand
#                         elif current_operator == '-':
#                             result_val = left_operand - right_operand
#                         result.append(result_val)
#     memo[input] = result
#     return memo[input]


def main():
    print("Expression evaluations: " +
          str(diff_ways_to_evaluate_expression("1+2*3")))

    print("Expression evaluations: " +
          str(diff_ways_to_evaluate_expression("2*3-4-5")))


main()
