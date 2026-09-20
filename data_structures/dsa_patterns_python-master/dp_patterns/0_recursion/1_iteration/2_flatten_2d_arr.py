# Recursive approach, iterative is very easy
# Tine: O(n) | Space: O(n) - note function keeps of adding to the stack from 1 column to another
def flatten_array(arr):
    def flatten_array_recursive(i, j):
        # base cases
        if i == rows:
            return
        # ** imp - base case 2
        if j == len(arr[i]):
            flatten_array_recursive(i + 1, 0)
            return
        result.append(arr[i][j])
        flatten_array_recursive(i, j + 1)
        return

    # main function
    rows = len(arr)
    result = []
    flatten_array_recursive(0, 0)
    return result


if __name__ == "__main__":
    arr = [[1, 2, 3], [4], [5, 6]]
    print(flatten_array(arr))
