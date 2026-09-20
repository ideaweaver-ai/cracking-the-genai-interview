# Copyright © 2020 way2FAANG


# we need to convert he array into Linked List and detect valid cycle
# How do we calculate the next node for a LL node ?
# based on the rule in problem: next_element_index = current_index + arr[current_index]


# Time: O(n**2) | Space: O(1)
def circular_array_loop_exists(arr):
    def find_next_index(current_index, start_direction):
        """Returns the next index based on the rules given in the problem.
        Returns -1 if cycle is invalid - case 1: one node cycle, case 2: direction changes in cycle"""
        # calculate next index
        next_index = (current_index + arr[current_index]) % n

        # now we need to check the two cases where cycle is invalid
        # check if current direction is same as previous direction
        current_direction = arr[current_index] > 0

        # case 1: one node cycle
        if next_index == current_index:
            next_index = -1

        # case 2: direction changes in cycle
        if current_direction != start_direction:
            next_index = -1

        return next_index

    # main function
    n = len(arr)

    # we have to check if there is a valid cycle from any array index
    for i in range(n):
        # check if we get a valid cycle starting from index i
        start_direction = arr[i] > 0
        slow, fast = i, i
        # we know there will be a cycle in a circular array - only question is it valid or invalid
        while True:
            slow = find_next_index(slow, start_direction)
            fast = find_next_index(fast, start_direction)

            # only if fast is not invalid need to calculate the 2nd next for fast
            if fast != -1:
                fast = find_next_index(fast, start_direction)

            # break if we get an invalid next index (-1) or cycle
            if slow == -1 or fast == -1:
                break
            if slow == fast:
                return True
            
    return False


if __name__ == '__main__':
    print(circular_array_loop_exists([1, 2, -1, 2, 2]))
    print(circular_array_loop_exists([2, 2, -1, 2]))
    print(circular_array_loop_exists([2, 1, -1, -2]))
