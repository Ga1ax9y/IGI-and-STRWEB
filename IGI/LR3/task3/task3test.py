from task3.task3 import *

def main():
    s = input("Введите строку: ")
    result = Uppercaseletters_find(s)
    print(f"Количество заглавных букв и цифр: {result}")
    #print(Uppercaseletters_find.__doc__)


if __name__ == "__main__":
    main()
