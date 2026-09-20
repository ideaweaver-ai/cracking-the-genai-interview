# Copyright © 2020 way2FAANG
# LeetCode: 449


from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Codec:
    # Time: O(n) | Space: O(n)
    def serialize(self, root: TreeNode) -> str:
        """Encodes a tree to a single string.
        """

        # Use Preorder
        def serializeHelper(root):
            # base case
            if root is None:
                return

            # process current node
            result.append(str(root.val))
            # recursion calls
            serializeHelper(root.left)
            serializeHelper(root.right)

        # main function
        result = []
        serializeHelper(root)
        return ','.join(result)

    def deserialize(self, data: str) -> TreeNode:
        """Decodes your encoded data to tree.
        """

        def deserializeHelper(lower, higher):
            # base case
            if not nodes_list:
                return None

            # Process current node
            root_val = int(nodes_list[0])

            # base case 2
            if root_val < lower or root_val > higher:
                return None

            root = TreeNode(root_val)
            nodes_list.popleft()

            # since preorder, left then right
            root.left = deserializeHelper(lower, root_val)
            root.right = deserializeHelper(root_val, higher)

            return root

        # main function
        nodes_list = deque()
        if data:
            nodes_list = deque(data.split(','))
        root = deserializeHelper(-float('inf'), float('inf'))
        return root

# Your Codec object will be instantiated and called as such:
# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# tree = ser.serialize(root)
# ans = deser.deserialize(tree)
# return ans