# Time: O(n) | Space: O(n)
def is_palindrome(string):
    def is_palindrome_helper(start, end):
        # base cases
        if start == end:
            return True
        if end == start+1:
            return string[start] == string[end]
        # recursion
        if string[start] != string[end]:
            return False
        return is_palindrome_helper(start+1, end-1)
    # main function
    return is_palindrome_helper(0, len(string)-1)


if __name__ == "__main__":
    print(is_palindrome("aba"))
    print(is_palindrome("abab"))
    print(is_palindrome("deced"))
