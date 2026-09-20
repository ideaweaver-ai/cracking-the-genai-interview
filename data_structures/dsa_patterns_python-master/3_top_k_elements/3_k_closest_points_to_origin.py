# Copyright © 2020 way2FAANG
# LeetCode: 973


from heapq import heappush, heappop


# class Point:
#
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def print_point(self):
#         print("[" + str(self.x) + ", " + str(self.y) + "] ", end='')
#
#
# def find_closest_points(points, k):
#     result = []
#     max_heap = []
#     # k closest points at start
#     for point in points[:k]:
#         dist = math.sqrt(point.x ** 2 + point.y ** 2)
#         heappush(max_heap, (-dist, point))  # max heap w.r.t dist
#     for point in points[k:]:
#         dist = math.sqrt(point.x ** 2 + point.y ** 2)
#         if dist < -max_heap[0][0]:
#             heappop(max_heap)
#             heappush(max_heap, (-dist, point))
#     # Create result
#     for i in range(k):
#         result.append(heappop(max_heap)[1])
#     return result


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # we implement __lt__ because heappush, heappop use < to compare (as they are min_heap based)
    def __lt__(self, other):
        # reverse sign - we are using max heap
        return self.calc_dist() > other.calc_dist()

    def calc_dist(self):
        return self.x ** 2 + self.y ** 2

    def print_point(self):
        print("[" + str(self.x) + ", " + str(self.y) + "] ", end='')


def find_closest_points(points, k):
    # heap should be reverse of what is required
    # for largest elements -> min heap, for smallest elements -> max heap
    # for this problem we use max heap since we require k closest points
    # the heap maintains the k closest points in the arr at any point of time
    max_heap = []

    # Iterate through the array and push elements into heap
    for point in points:
        heappush(max_heap, point)
        # we want to store only k largest/ smallest elements
        # so, ensure heap len is always k
        if len(max_heap) > k:
            heappop(max_heap)

    return list(max_heap)


def main():
    result = find_closest_points([Point(1, 3), Point(3, 4), Point(2, -1)], 2)
    print("Here are the k points closest the origin: ", end='')
    for point in result:
        point.print_point()


main()
