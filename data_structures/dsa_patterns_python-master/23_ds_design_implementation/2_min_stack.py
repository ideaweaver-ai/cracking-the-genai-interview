# Copyright © 2020 way2FAANG
# LeetCode: 155
# Level: easy

class MinStack:
    # Space: O(n)
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.min_stack = []

    # Time: O(1)
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(self.min_stack[-1], val))

    # Time: O(1)
    def pop(self) -> None:
        if len(self.stack) == 0:
            return None  # error
        val = self.stack.pop()  # pops last element by default
        self.min_stack.pop()
        return val

    # Time: O(1)
    def top(self) -> int:
        if len(self.stack) == 0:
            return None  # error
        return self.stack[-1]

    # Time: O(1)
    def getMin(self) -> int:
        if len(self.min_stack) == 0:
            return None  # error
        return self.min_stack[-1]

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
