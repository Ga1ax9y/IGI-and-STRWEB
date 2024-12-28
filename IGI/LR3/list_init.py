import random
INPUT_ERROR = "Ошибка ввода! Повторите еще раз"
def generate(a,size):
    count = 0
    i = a
    while count <= size:
        yield i
        i+=1
        count+=1

def user_init(arr):
    '''Function for initializing the list by the user

    Keyword argument:
    arr -- list

    Return value:
    arr -- inizialized list

    '''
    while True:
        try:
            size = int(input("Введите размер списка: "))
            if size <=0:
                raise ValueError
            break
        except ValueError:
            print(INPUT_ERROR)
    for i in range(size):
        while True:
            try:
                num = float(input(f"Введите {i+1}-й элемент списка: "))
                break
            except ValueError:
                print(INPUT_ERROR)
        arr.append(num)
    return arr

def rand_init(arr):
    '''Function for initializing the list with random values

    Keyword argument:
    arr -- list

    Return value:
    arr -- inizialized list

    '''
    while True:
        try:
            size = int(input("Введите размер списка: "))
            break
        except ValueError:
            print(INPUT_ERROR)
    for x in generate(5,size):
        arr.append(x)
    return arr
