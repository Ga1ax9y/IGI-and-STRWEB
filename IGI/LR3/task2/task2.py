INPUT_ERROR = "Ошибка ввода! Повторите еще раз"

def my_decorator(func):
    def something():
        print("Начало")
        result = func()
        print("Конец")
        return result
    return something

@my_decorator
def Multiplication():
    """The function takes integers and multiplies them.

    The end of the cycle is the input of a positive number.

    Return value:
    result -- the product of the entered numbers

    """
    result = 1
    while True:
        try:
            n = int(input("Введите целое число: "))
            break
        except ValueError:
            print(INPUT_ERROR)
    while n <= 0:
        result *=n
        while True:
            try:
                n = int(input("Введите целое число: "))
                break
            except ValueError:
                print(INPUT_ERROR)
    return result
