def find_gcd(a, b):
    # base cases
    if b == 0:
        return a
    # recursion
    return find_gcd(b, a % b)


if __name__ == "__main__":
    print( find_gcd(320, 104))
    print(find_gcd(100, 10))
