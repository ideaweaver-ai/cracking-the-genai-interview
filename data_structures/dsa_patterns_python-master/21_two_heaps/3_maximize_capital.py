from heapq import heappush, heappop


# Time: O(n*log(n) + O(n*k) k-num of projects to be selected, Space: O(n) - for the zip
def find_maximum_capital(capital, profits, numberOfProjects, initialCapital):
    capitals_profits = list(zip(capital, profits))
    capitals_profits.sort()

    for _ in range(numberOfProjects):
        # select project giving max profit
        max_project_profit = 0
        for cap, prof in capitals_profits:
            if cap > initialCapital:
                break
            max_project_profit = max(max_project_profit, prof)

        # add profit of the max project
        initialCapital += max_project_profit

    return initialCapital


# Time: O(n*log(n) + O(n*k*log(n)) k-num of projects to be selected, Space: O(n) - for the heap - Is this better algo ??
def find_maximum_capital(capitals, profits, numberOfProjects, initialCapital):
    min_heap_capital = []
    max_heap_capital = []
    available_capital = initialCapital

    # insert all project capitals to a min-heap
    for i in range(len(capitals)):
        heappush(min_heap_capital, (capitals[i], i))

    for _ in range(numberOfProjects):
        # find all projects that can be selected within the available capital and insert them in a max-heap
        while min_heap_capital and min_heap_capital[0][0] <= available_capital:
            _, i = heappop(min_heap_capital)
            heappush(max_heap_capital, -profits[i])

        # terminate if we are not able to find any project that can be completed within the available capital
        if not max_heap_capital:
            break

        # select the project with the maximum profit
        # should it be heappop or just add -max_heap[0] - as project can be selected multiple times
        available_capital += -heappop(max_heap_capital)
    return available_capital


def main():
    print("Maximum capital: " +
          str(find_maximum_capital([0, 1, 2], [1, 2, 3], 2, 1)))
    print("Maximum capital: " +
          str(find_maximum_capital([0, 1, 2, 3], [1, 2, 3, 5], 3, 0)))


main()
