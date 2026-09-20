def find_stair_step_combinations(n):
    # BF
    # Time: O(3**n) | Space: O(n)
    def find_stair_step_combinations_helper(i, current_path):
        # base cases
        if i == n:
            result.append(list(current_path))
            return
        if i > n:
            return

        # process current_node
        current_path.append(i)
        # recursive calls
        find_stair_step_combinations_helper(i+1, current_path)
        find_stair_step_combinations_helper(i + 2, current_path)
        find_stair_step_combinations_helper(i + 3, current_path)

        # backtrack
        del current_path[-1]

    # main function
    result = []
    find_stair_step_combinations_helper(0, [])
    return result


if __name__ == "__main__":
    print(find_stair_step_combinations(4))