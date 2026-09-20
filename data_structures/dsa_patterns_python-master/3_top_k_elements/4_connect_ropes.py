# Copyright © 2020 way2FAANG
# LeetCode: 321


from heapq import heappush, heappop, heapify


# Time O(n*log(n)) | Space: O(n)
def minimum_cost_to_connect_ropes(ropeLengths):
    # Input validations
    if not ropeLengths:
        return 0

    if len(ropeLengths) < 2:
        return ropeLengths[0]

    # Output var
    total_cost = 0

    # O(n) this way | instead of pushing elements one by one into new min heap which is O(n*log(n))
    heapify(ropeLengths)  # heapify is in place

    # O(n * log(n))
    while len(ropeLengths) >= 2:
        rope1 = heappop(ropeLengths)
        rope2 = heappop(ropeLengths)

        new_rope = rope1 + rope2
        total_cost += new_rope

        heappush(ropeLengths, new_rope)

    return total_cost


def main():
    print("Minimum cost to connect ropes: " +
          str(minimum_cost_to_connect_ropes([1, 3, 11, 5])))
    print("Minimum cost to connect ropes: " +
          str(minimum_cost_to_connect_ropes([3, 4, 5, 6])))
    print("Minimum cost to connect ropes: " +
          str(minimum_cost_to_connect_ropes([1, 3, 11, 5, 2])))


main()


def main():
    print("Minimum cost to connect ropes: " +
          str(minimum_cost_to_connect_ropes([1, 3, 11, 5])))
    print("Minimum cost to connect ropes: " +
          str(minimum_cost_to_connect_ropes([3, 4, 5, 6])))
    print("Minimum cost to connect ropes: " +
          str(minimum_cost_to_connect_ropes([1, 3, 11, 5, 2])))


main()
