from task5f import *

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
    A = ()
    print("1.Создать матрицу\n2.Создать массив\n")
    choise = check_error("Выберите вариант: ")
    if choise == 1:
        while True:
            try:
                n = check_error("Введите n: ")
                m = check_error("Введите m: ")
                max_value = check_error("Введите максимальное значение: ")
                A = NumpyResearch.create_matrix(n,m,max_value)
                break
            except ValueError:
                print(input_error)
        print(A)
    elif choise == 2:
        while True:
            try:
                n = check_error("Введите минимальное число: ")
                m = check_error("Введите максимальное число: ")
                size = check_error("Введите размерность массива: ")
                A = NumpyResearch.create_array(n,m,size)
                break
            except ValueError:
                print(input_error)
        print(A)
    else:
        print("Ошибка ввода")
        return

    print("1.Вывести элемент массива\n2.Вывести разрез массива\n3.Универсальные функции")
    choise = check_error("Выберите вариант: ")
    if choise == 1:
        while True:
            try:
                num = check_error("Введите индекс элемена массива: ")
                print(NumpyResearch.index_array(A,num))
                break
            except ValueError:
                print(input_error)
    if choise == 2:
        while True:
            try:
                start = check_error("Введите начало среза: ")
                end = check_error("Введите конец среза: ")
                step = check_error("Введите шаг: ")
                print(NumpyResearch.slice_array(A,start,end,step))
                break
            except ValueError:
                print(input_error)
    if choise == 3:
        print("========================================")
        print("Библиотека NumPy")
        print("1.Сложить два массива\n2.Массив в степени:\n3.Синусы массива\n4.Корень массива")
        print("========================================")
        print("Математические и статистические операции")
        print("5.Среднее значение элементов массива\n6.Медиана\n7.Корреляция\n8.Дисперсия\n9.Стандартное отклонение\n10.Cумма модулей отрицательных нечетных элементов")
        print("========================================")
        uni_choise = check_error("Выберите вариант: ")
        if uni_choise == 1:
            new_arr = A * 2
            print("Первый массив:\n", A)
            print("Второй массив:\n",new_arr)
            print(NumpyResearch.sum_2_arrays(A,new_arr))
        elif uni_choise == 2:
            print("Первый массив:\n", A)
            power = check_error("Введите степень: ")
            print(NumpyResearch.power_array(A,power))
        elif uni_choise == 3:
            print("Первый массив:\n", A)
            print(NumpyResearch.sin_of_array(A))
        elif uni_choise == 4:
            print("Первый массив:\n", A)
            print(NumpyResearch.sqrt_of_array(A))
        elif uni_choise == 5:
            print("Первый массив:\n", A)
            print(NumpyResearch.array_mean(A))
        elif uni_choise == 6:
            print(NumpyResearch.array_median(A))
        elif uni_choise == 7:
            new_arr = A - 25
            print("Первый массив:\n", A)
            print("Второй массив:\n",new_arr)
            print(NumpyResearch.array_corr(A,new_arr))
        elif uni_choise == 8:
            print("Первый массив:\n", A)
            print(NumpyResearch.arrray_variance(A))
        elif uni_choise == 9:
            print("Первый массив:\n", A)
            print(NumpyResearch.array_std(A))
            print(NumpyResearch.my_array_std(A))
        elif uni_choise == 10:
            arr = np.array([12,-3,-6,34,-75,-43,11,100])
            print("Исходный массив:", arr)
            print(NumpyResearch.sum_neg_odd(arr))
        else:
            print("Ошибка ввода")
            return
    else:
        print("Ошибка ввода")
        return


if __name__ == "__main__":
    main()
