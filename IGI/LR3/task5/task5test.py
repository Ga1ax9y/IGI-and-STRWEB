from task5.task5 import *

def main():
    arr = []
    n = int(input("Введите количество элементов списка: "))
    for i in range(n):
        d = float(input(f"Введите {i+1} элемент списка: "))
        arr.append(d)
    print(f"Номер минимального по модулю элемента: {Min_modul(arr)}")
    print(f"Сумма элементов списка после первого положительного элемента: {Sum_after(arr)}")

if __name__ == "__main__":
    main()

