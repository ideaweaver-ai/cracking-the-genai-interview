# Copyright © 2020 way2FAANG
# LeetCode: 202


# Check out the time complexity calc. It's not straight forward
def find_happy_number(num):
    def cal_squared_sum_digits(num):
        sum_ = 0
        while num != 0:
            digit = num % 10
            num = num // 10
            sum_ += digit ** 2
        return sum_

    slow, fast = num, num
    while True:
        slow = cal_squared_sum_digits(slow)
        fast = cal_squared_sum_digits(cal_squared_sum_digits(fast))
        if slow == fast:  # each number has to have a cycle
            break
    return slow == 1  # if cycle is at 1, num is happy else it is not happy


def main():
    print(find_happy_number(23))
    print(find_happy_number(12))


main()
