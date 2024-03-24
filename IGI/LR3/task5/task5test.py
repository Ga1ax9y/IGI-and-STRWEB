from task5.task5 import *
from list_init import *
def main():
    while True:
        arr = []
        choise = int(input("Выберите вариант:\n1.Заполнить список автоматически\n2.Заполнить список вручную\n"))
        if choise == 1:
            arr = rand_init(arr)
            print_list(arr)
            break
        elif choise == 2:
            arr = user_init(arr)
            print_list(arr)
            break
        else:
            print("Ошибка ввода!")

    print(f"Номер минимального по модулю элемента: {Min_modul(arr)}")
    print(f"Сумма элементов списка после первого положительного элемента: {Sum_after(arr)}")
    #print(Min_modul.__doc__, Sum_after.__doc__ )


if __name__ == "__main__":
    main()
