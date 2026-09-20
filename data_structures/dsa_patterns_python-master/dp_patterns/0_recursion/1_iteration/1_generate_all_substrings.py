# Time: O(n**3) | Space: (n + n-1 + n-2...1) = O(n**2)
def generate_all_substrings(string):
    n = len(string)
    result = []
    for i in range(n):
        for j in range(i, n):
            result.append(string[i:j+1])  # O(n)
    return result


# Time: O(n**3) | Space: O(n)
def generate_all_substrings_rec(string):
    def iterate_first_chars(i):
        # base case
        if i == n:
            return
        # recursion
        iterate_second_chars(i, i)
        iterate_first_chars(i+1)

    def iterate_second_chars(i, j):
        # base cases
        if j == n:
            return
        result.append(string[i:j+1]) # O(n)
        iterate_second_chars(i, j+1)


    # main function
    n = len(string)
    result = []
    iterate_first_chars(0)
    return result


# Using single recursive function
def generate_all_substrings_rec(string):

    def gen_substring_helper(i, j):
        # base cases
        if i == n:
            return
        if j == n:
            gen_substring_helper(i+1, i+1)
            return

        result.append(string[i:j+1])  # O(n)
        gen_substring_helper(i, j+1)


    # main function
    n = len(string)
    result = []
    gen_substring_helper(0, 0)
    return result


if __name__ == "__main__":
    print(generate_all_substrings("time"))
    print(generate_all_substrings_rec("time"))