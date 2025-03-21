def merge(a: list, b: list) -> list:
    '''
    Объединяет два отсортированных массива
    в один отсортированый массив
    '''
    i = 0
    j = 0
    sorted_array = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            sorted_array.append(a[i])
            i += 1
        else:
            sorted_array.append(b[j])
            j += 1
    sorted_array += a[i:]
    sorted_array += b[j:]
    return sorted_array

print(merge(a=[1, 3, 5, 8], b=[2, 6, 7, 13]))
