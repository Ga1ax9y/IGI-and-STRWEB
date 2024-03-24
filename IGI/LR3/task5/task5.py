def Min_modul(arr):
    """Function for finding the number of the minimum modulo element

    Keyword argument:
    arr -- list

    Return value:
    min_mod -- the number of the minimum modulo element

    """
    min_mod = arr.index((min(arr,key=abs)))+1
    return min_mod

def Sum_after(arr):
    '''Function for finding sum of the list items after first positive element

    Keyword argument:
    arr -- list

    Return value:
    result - sum of the list items after the first positive element

    '''
    result = 0
    first = -228
    for i in range(len(arr)):
        if arr[i] > 0:
            first = i+1
            break
    if first != -228:
        for num in arr[first:]:
            result +=num
        return result
    else: return 0

def print_list(arr):
    """Function for printing elements of list

    Keyword argument:
    arr -- list

    """
    print("Элементы получившегося списка: ",*arr)
