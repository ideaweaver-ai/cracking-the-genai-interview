"""Run all examples or one: python 12_functions.py immutable_values"""


def change_immutable(number, price, text, enabled):
    number += 1
    price += 0.5
    text = text.upper()
    enabled = not enabled
    print("inside:", number, price, text, enabled)


def immutable_values():
    count, cost, name, active = 3, 4.5, "ada", True
    change_immutable(count, cost, name, active)
    # Rebinding immutable values inside a function does not change the caller's names.
    print("outside:", count, cost, name, active)


def add_to_list(items):
    items.append("new item")


def update_dictionary(profile):
    profile["level"] = "beginner"


def mutable_collections():
    shopping_list = ["milk"]
    learner = {"name": "Ada"}
    add_to_list(shopping_list)
    update_dictionary(learner)
    # The function can mutate the same list or dictionary object seen by the caller.
    print(shopping_list, learner)


def third_function():
    print("3. third_function runs at the top of the call stack")


def second_function():
    print("2. second_function calls third_function")
    third_function()
    print("4. third_function returned to second_function")


def first_function():
    print("1. first_function calls second_function")
    second_function()
    print("5. second_function returned to first_function")


def function_call_stack():
    first_function()
    # Each call is added to the stack; functions return in reverse call order.

def sum_of_numbers(num1, num2):
    print("num1: ", num1)
    print("num2: ", num2)
    print("sum: ", num1 + num2)
    return num1 + num2


# EXAMPLES = {
#     "immutable_values": immutable_values,
#     "mutable_collections": mutable_collections,
#     "call_stack": function_call_stack,
# }

if __name__ == "__main__":
    # import sys

    # for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
    #     EXAMPLES[example]()

    print(sum_of_numbers(100, 200))
