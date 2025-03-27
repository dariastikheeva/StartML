import random

def kth_largest(array, k):
    def partition(array, left, right, pivot_index):
        pivot_value = array[pivot_index]
        array[pivot_index], array[right] = array[right], array[pivot_index]
        store_index = left
        for i in range(left, right):
            if array[i] < pivot_value:
                array[store_index], array[i] = array[i], array[store_index]
                store_index += 1
        array[right], array[store_index] = array[store_index], array[right]
        return store_index

    def quickselect(array, left, right, k_smallest):
        if left > right:
            return None

        if left == right:
            return array[left]

        pivot_index = random.randint(left, right)
        pivot_index = partition(array, left, right, pivot_index)

        if k_smallest == pivot_index:
            return array[k_smallest]
        elif k_smallest < pivot_index:
            return quickselect(array, left, pivot_index - 1, k_smallest)
        else:
            return quickselect(array, pivot_index + 1, right, k_smallest)

    return quickselect(array, 0, len(array) - 1, len(array) - k)
