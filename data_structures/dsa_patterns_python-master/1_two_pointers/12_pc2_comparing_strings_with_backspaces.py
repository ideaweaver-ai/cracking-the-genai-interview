# Time: O(N+M), N-length of string1, M-length of string2; Space: O(1) space
def backspace_compare(str1, str2):
    p1, p2 = len(str1) - 1, len(str2) - 1
    while p1 >= 0 and p2 >= 0:
        p1 = next_non_backspace_char(str1, p1)
        p2 = next_non_backspace_char(str2, p2)
        # check if both the strings have ended
        if p1 < 0 and p2 < 0:
            # don't need to check specifically for -1
            # sometimes we may have extra backspaces e.g ##xyz - our function will return -2 when i reaches 1
            # but it still means the string ended
            return True
        # One string ended but other didn't
        if p1 < 0 or p2 < 0:
            return False

        # both pointers p1 and p2 are valid
        if str1[p1] != str2[p2]:
            return False

        p1 -= 1
        p2 -= 1

    return True


def next_non_backspace_char(str_, i):
    """Returns the index of next non backspace char """
    num_backspaces = 0
    while i >= 0:
        if str_[i] == '#':
            num_backspaces += 1
        # Don't complicate the logic, use power of elif
        # if we are evaluating elif means we have a valid char
        # so we need to check if num_backspaces > 0
        elif num_backspaces > 0:
            num_backspaces -= 1
        else:
            # since we don't have any backspaces remaining, we have found valid char
            break
        i -= 1

    return i
