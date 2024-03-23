from task1.task1 import *
from math import log
from prettytable import PrettyTable

INPUT_ERROR = "Ошибка ввода! Повторите еще раз"

def main():
    while True:
        try:
            x = int(input("Введите значение аргумента: "))
            break
        except ValueError:
            print(INPUT_ERROR)
    while True:
        try:
            eps = float(input("Введите точность вычислений: "))
            break
        except ValueError:
            print(INPUT_ERROR)

    table = PrettyTable()
    table.field_names = ["x", "n", "F(x)", "Math F(x)","eps"]
    cor = powerSeries(x,eps)
    table.add_row([x, cor[1], cor[0], log((x+1)/(x-1)), eps])
    print(table)
    #print(PowerSeries.__doc__)


if __name__ == "__main__":
    main()
