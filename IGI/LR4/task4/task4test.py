from task4.task4f import *

input_error = "Ошибка ввода! Повторите попытку"
def check_error(text):
    while True:
        try:
            value = int(input(text))
            return value
            break
        except ValueError:
            print(input_error)

def main():
    diag1 = check_error("Введите размер первой диагонали: ")
    diag2 = check_error("Введите размер первой диагонали: ")
    angle = check_error("Введите угол между ними (в градусах): ")
    while True:
        try:
            col = input("Введите цвет фигуры: ")
            a = Parallelogram(diag1,diag2,angle,col)
            break
        except ValueError:
            print("Ошибка выбора цвета")

    print(a.get_info())
    name = input("Введите имя фигуры: ")
    a.draw(name)


if __name__ == "__main__":
    main()
