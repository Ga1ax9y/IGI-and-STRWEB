from prettytable import PrettyTable
from task3.task3f import *
from task3.SeriesDrawer import *

INPUT_ERROR = "Ошибка ввода! Повторите еще раз"

def main():
    while True:
        try:
            x = int(input("Введите значение аргумента: "))
            if x == 1:
                raise ValueError
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
    a = PowerSeriesExtended(x,eps)
    cor = a.calculate()
    table.add_row([x, cor[1], cor[0], log((x+1)/(x-1)), eps])
    print(table)

    a.get_metrics()
    dr = Drawer(a)
    dr.draw_series()



if __name__ == "__main__":
    main()
