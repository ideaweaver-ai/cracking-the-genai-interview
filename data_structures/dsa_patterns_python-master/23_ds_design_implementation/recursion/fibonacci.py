
def fibonacci_recursive(n: int) -> int:
    # base case
    if n == 0 or n == 1:
        return n

    # Recursion
    return fibonacci_recursive(n-1)+fibonacci_recursive(n-2)


def fibonacci_iterative(n: int) -> int:
    stack = []
    sum = 0
    stack.append(n)

    while stack:
        n = stack.pop()
        if n == 0 or n == 1:
            sum += n
        else:
            stack.append(n-1)
            stack.append(n-2)
    return sum


if __name__ == '__main__':
    # print(fibonacci_recursive(10))
    print(fibonacci_iterative(10))