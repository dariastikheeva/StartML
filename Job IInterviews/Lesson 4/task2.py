class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invert_tree(head):
    if head is None:
        return None

    head.left, head.right = head.right, head.left

    invert_tree(head.left)
    invert_tree(head.right)

    return head
