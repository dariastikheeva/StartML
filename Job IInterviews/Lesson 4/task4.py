class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def kth_smallest(head, k):
    def inorder(node):
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)

    sorted_arr = inorder(head)
    return sorted_arr[k-1]
