# class Node:
#     def __init__(self, value, next=None):
#         self.value = value
#         self.next = next

def rotate_right(head, k: int):
    if not head or not head.next or k == 0:
        return head

    # Определяем длину списка
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    # k может быть больше, чем длина списка
    k = k % length

    if k == 0:
        return head

    # Ищем новый head
    current = head
    for i in range(length - k - 1):
        current = current.next

    # Поворачиваем список
    new_head = current.next
    current.next = None
    tail.next = head

    return new_head
