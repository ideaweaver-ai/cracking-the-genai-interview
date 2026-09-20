# Euler's algorithm

def find_gcd(a, b):
    # For Euler's algo a > b
    if b > a:
        # swap
        b, a = a, b
    # base case
    if b == 0:
        return a
    return find_gcd(b, a % b)


if __name__ == "__main__":
    print(find_gcd(8, 2))