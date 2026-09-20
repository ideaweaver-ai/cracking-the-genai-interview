class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1  # we need height for balancing avl

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


class AVLTree:

    def insert(self, root, key):

        # normal bst insert
        if root is None:
            return TreeNode(key)

        if key <= root.val:
            root.left = self.insert(root.left, key)

        elif key > root.val:
            root.right = self.insert(root.right, key)

        # update height
        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1

        # find balance
        balance = self.get_balance(root)

        # balance the tree
        # 4 cases
        # Left left
        if balance > 1 and key < root.left.val:
            root = self.rotate_right(root)

        # Left Right
        elif balance > 1 and key > root.left.val:
            root.left = self.rotate_left(root.left)
            root = self.rotate_right(root)

        # Right Right
        if balance < -1 and key > root.right.val:
            root = self.rotate_left(root)

        # Right Left
        elif balance < -1 and key < root.right.val:
            root.right = self.rotate_right(root.right)
            root = self.rotate_left(root)

        return root

    def get_height(self, root):
        """To wrap the None case"""
        if root is None:
            return 0
        return root.height

    def get_balance(self, root):
        return self.get_height(root.left) - self.get_height(root.right)

    def rotate_left(self, root):
        # temp references
        child = root.right
        s3 = child.left

        # rotate
        child.left = root
        root.right = s3

        # update height - if not updated balance will be incorrect in next iteration
        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1
        child.height = max(self.get_height(child.left), self.get_height(child.right)) + 1

        return child

    def rotate_right(self, root):
        # temp references
        child = root.left
        s3 = child.right

        # rotate
        child.right = root
        root.left = s3

        # update height - if not updated balance will be incorrect in next iteration
        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1
        child.height = max(self.get_height(child.left), self.get_height(child.right)) + 1

        return child


if __name__ == '__main__':
    myTree = AVLTree()
    root = None
    root = myTree.insert(root, 10)
    root = myTree.insert(root, 20)
    root = myTree.insert(root, 30)
    root = myTree.insert(root, 40)
    root = myTree.insert(root, 50)
    root = myTree.insert(root, 25)
    root.display()

    root = myTree.insert(root, 60)
    root.display()
