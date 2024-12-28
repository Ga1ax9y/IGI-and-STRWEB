from task4.task4f import *
from my_input import check_error,input_error
import matplotlib.colors as mcolors

def main():
    diag1 = check_error("Введите размер первой диагонали: ")
    diag2 = check_error("Введите размер первой диагонали: ")
    angle = check_error("Введите угол между ними (в градусах): ")
    while True:
        try:
            col = input("Введите цвет фигуры: ")
            mcolors.to_rgb(col)
            break
        except ValueError:
            print("Ошибка выбора цвета")

    a = Parallelogram(diag1,diag2,angle,col)
    print(a.get_info())
    name = input("Введите имя фигуры: ")
    a.draw(name)


if __name__ == "__main__":
    main()
