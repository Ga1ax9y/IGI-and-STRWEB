import task1.task1test as task1
import task2.task2test as task2
import task3.task3test as task3
import task4.task4test as task4
import task5.task5test as task5
from prettytable import PrettyTable

def main():
    table = PrettyTable()
    table.field_names = ["Номер задания", "Краткое описание"]
    table.add_row([1,"Вычисление значения функции c помощью разложения функции в степенной ряд"], divider=True)
    table.add_row([2,"Цикл, который принимает целые числа и умножает их"], divider=True)
    table.add_row([3,"Количество заглавных букв и цифр"], divider=True)
    table.add_row([4,"Количество слов в строке, самое длинное слово, вывод нечетных слов"], divider=True)
    table.add_row([5,"Номер минимального по модулю элемента и сумма элементов списка после первого положительного"])
    while True:
        print(table)
        choise = input("Выберите номер задания: ")
        user_func = "task" + choise + "." +"main()"
        eval(user_func)
        restart = input("Хотите продолжить (y/N)?")
        if restart == "N":
            break







if __name__ == "__main__":
    main()
