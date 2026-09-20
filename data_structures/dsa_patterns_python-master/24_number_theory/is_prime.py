from math import sqrt


def is_prime(n):
    if n == 1:
        return False
    elif n == 2:
        return True
    for i in range(2, int(sqrt(n))):
        if n % i == 0:
            return False

    return True


if __name__ == "__main__":
    print(is_prime(1))
    print(is_prime(2))
    print(is_prime(3))
    print(is_prime(11))
    print(is_prime(12))
    print(is_prime(13))
    print(is_prime(37))
