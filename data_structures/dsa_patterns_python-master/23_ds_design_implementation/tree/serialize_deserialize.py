from collections import deque
from tree.bst_print import TreeNode

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return ''
        result = []
        queue = deque()
        queue.append(root)
        while queue:
            current_node = queue.popleft()
            if current_node:
                result.append(current_node.val)
                queue.append(current_node.left)
                queue.append(current_node.right)
            else:
                result.append(None)

        result = ','.join(str(s) for s in result)
        return result

    def convertToNode(self, val):
        if val == 'None':
            return None
        else:
            return TreeNode(int(val))

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None
        data = data.split(',')
        return self.deserializeHelper(data, 0)

    def deserializeHelper(self, data, index):
        """data - cleaned version"""
        if index >= len(data):
            return None

        current_node = self.convertToNode(data[index])
        if current_node is not None:
            left_index = 2 * index + 1
            right_index = 2 * index + 2
            if left_index < len(data):
                current_node.left = self.deserializeHelper(data, left_index)
            if right_index < len(data):
                current_node.right = self.deserializeHelper(data, right_index)

        return current_node

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.deserialize(codec.serialize(root))


if __name__ == '__main__':
    root = TreeNode(5)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = None
    root.left.right = None
    root.right.left = TreeNode(2)
    root.right.right = TreeNode(4)
    root.right.left.left = TreeNode(3)
    root.right.left.right = TreeNode(1)
    codec = Codec()
    result = codec.serialize(root)
    print(type(result))
    print(result)
    codec.deserialize(codec.serialize(root)).display()