# Time: O(n) | Space: O(n)
def count_moves(n):
    """Return number of moves to shift n disks in ascending order to another pole, given a temporary pole"""
    # base cases
    if n == 1:
        return 1
    return 2 * count_moves(n - 1) + 1


if __name__ == "__main__":
    print(count_moves(4))
