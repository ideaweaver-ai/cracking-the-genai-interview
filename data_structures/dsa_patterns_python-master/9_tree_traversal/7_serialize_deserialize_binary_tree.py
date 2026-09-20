# Copyright © 2020 way2FAANG
# LeetCode: 297


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def display(self):
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.val
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class Codec:
    # Time: O(n**2)-  O(n) visit every node, O(n) - copy string
    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """

        def serialize_helper(current_node, string):
            """Returns string representation of subtree with current node as root"""
            # base case
            if current_node is None:
                string += "None,"
                return string

            # process current node
            string += str(current_node.val) + ','  # O(n)

            # recursive calls
            string = serialize_helper(current_node.left, string)
            string = serialize_helper(current_node.right, string)

            # return
            return string

        # main function
        string = serialize_helper(root, "")
        return string

    # Time: O(n**2)-  O(n) visit every node, O(n) - pop index 0 from list
    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """

        def deserialize_helper(nodes_list):
            """Returns root of the subtree with the nodes_list given as input"""
            # base case
            if not nodes_list:
                return None

            # process current node
            current_node_val = nodes_list.pop(0)
            if current_node_val == 'None':
                current_node = None
            else:
                current_node = TreeNode(current_node_val)

            if current_node:
                current_node.left = deserialize_helper(nodes_list)
                current_node.right = deserialize_helper(nodes_list)

            return current_node

        # main function
        nodes_list = []
        if data:
            nodes_list = data[:-1].split(',')

        return deserialize_helper(nodes_list)


from collections import deque


class Codec:
    # Time: O(n) - visit every node
    # Space: O(n) - recursion function stack
    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """

        def serialize_helper(current_node):
            """Returns string representation of subtree with current node as root"""
            # base case
            if current_node is None:
                string.append("None")
                return

            # process current node
            string.append(str(current_node.val))

            # recursive calls
            serialize_helper(current_node.left)
            serialize_helper(current_node.right)

        # main function
        string = []
        serialize_helper(root)

        # return as a string
        return ",".join(string)  # O(n)

    # Time: O(n) visit every node
    # Space: O(n) - recursion function stack
    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """

        def deserialize_helper(nodes_list):
            """Returns root of the subtree with the nodes_list given as input"""
            # base case
            if not nodes_list:
                return None

            # process current node
            current_node_val = nodes_list.popleft()
            if current_node_val == 'None':
                current_node = None
            else:
                current_node = TreeNode(current_node_val)

                # recursive calls
                current_node.left = deserialize_helper(nodes_list)
                current_node.right = deserialize_helper(nodes_list)

            return current_node

        # main function
        nodes_list = deque()
        if data:
            nodes_list = deque(data.split(','))  # O(n)

        return deserialize_helper(nodes_list)


if __name__ == '__main__':
    # Your Codec object will be instantiated and called as such:
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    ser = Codec()
    deser = Codec()
    ans = deser.deserialize(ser.serialize(root))
    ans.display()
