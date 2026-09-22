# O(N) time | O(1) space
def dutch_flag_sort(arr):
    # Indexes point to where next 0 and 2 element should be put
    # all elements < next_zero should be 0, all elements > next_two should be 2
    # once we put 0 and 2 in their right places, 1 will automatically be in its right place
    next_zero, next_two = 0, len(arr) - 1
    i = 0
    # imp condition for termination
    while i <= next_two:
        if arr[i] == 0:
            # swap with element at next_zero index
            arr[next_zero], arr[i] = arr[i], arr[next_zero]
            # increment next_zero
            next_zero += 1
            # the element at next_zero has to be 1 ?
            # when we are at i all elements before i have been put in their correct place
            # so element at next_zero has to be 1
            # hence we can increment i also
            i += 1
        elif arr[i] == 2:
            # swap with element at next_two index
            arr[next_two], arr[i] = arr[i], arr[next_two]
            # decrement next_two
            next_two -= 1
            # since this element could be 0 or 2 we cannot move to next element
            # if after swapping this element becomes 0 we need to put it in its right place
        else:
            # arr[i] == 1
            i += 1

    return arr


def main():
    # arr = [1, 0, 2, 1, 0]
    # dutch_flag_sort(arr)
    # print(arr)

    arr = [2, 2, 0, 1, 2, 0]
    dutch_flag_sort(arr)
    print(arr)


main()
