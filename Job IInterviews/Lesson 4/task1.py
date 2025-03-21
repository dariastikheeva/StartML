class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def are_trees_equal(head_1, head_2):
    if not head_1 and not head_2:
        return True
    if not head_1 or not head_2:
        return False
    if head_1.val != head_2.val:
        return False
    return are_trees_equal(head_1.left, head_2.left) and are_trees_equal(head_1.right, head_2.right)
