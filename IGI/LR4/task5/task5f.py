import numpy as np

class NumpyResearch():

    @classmethod
    def create_matrix(self, n, m, max_value):
        if n > 0 and m > 0:
            rng = np.random.default_rng()
            arr =rng.integers(max_value,size=(n,m))
            return arr
        else:
            raise ValueError

    @classmethod
    def create_array(self, n, m, size):
        if size > 0 :
            arr = np.random.randint(n,m,size)
            return arr
        else:
            raise ValueError

    @classmethod
    def index_array(self, your_arr, index):
        if -(len(your_arr)) <=index <= len(your_arr)-1:
            print("Исходный массив: ",your_arr)
            print(f"Элемент номер {index}: ",end="")
            return your_arr[index]
        else:
            raise ValueError


    @classmethod
    def slice_array(self, your_arr, start, end, step = 1)->np.array:
        print("Исходный массив: ",your_arr)
        if (0 <= start <= len(your_arr)) and (0 <= end <= len(your_arr)):
            print(f"Срез от [{start},{end}) с шагом: {step}: ",end="" )
            return your_arr[start:end:step]
        else:
            raise ValueError

    @classmethod
    def sum_2_arrays(self, arr1, arr2):
        print("Сумма двух массивов: ")
        return np.add(arr1,arr2)

    @classmethod
    def power_array(self, arr, power):
        print(f"Массив в степени {power}: ",end="")
        return np.power(arr,power)

    @classmethod
    def sin_of_array(self, arr):
        print("Синусы массива: ",end="")
        return np.sin(arr)

    @classmethod
    def sqrt_of_array(self, arr):
        print("Корень из массива: ",end="")
        return np.sqrt(arr)

    @classmethod
    def array_mean(self, arr):
        print("Среднее значение элементов массива: ", end="")
        return np.mean(arr)

    @classmethod
    def array_median(self, arr):
        print("Медиана массива: ",end="")
        return np.median(arr)

    @classmethod
    def array_corr(self,arr1,arr2):
        print("Коэффициент корреляции: ",end="")
        return np.corrcoef(arr1,arr2)

    @classmethod
    def arrray_variance(self,arr):
        print("Дисперсия массива: ", end="")
        return np.var(arr)

    @classmethod
    def array_std(self,arr):
        print("Стандартное отклонение (numpy): ",end="")
        return np.std(arr)

    @classmethod
    def sum_neg_odd(self,arr):
        neg_odd_elements = arr[(arr < 0 ) & (arr % 2 !=0)]
        sum_of_abs = np.sum(np.abs(neg_odd_elements))
        print("Cумма модулей отрицательных нечетных элементов: ",end="")
        return sum_of_abs

    @classmethod
    def my_array_std(self,arr):
        mean_value = np.mean(arr)
        squared_diff = np.power(arr - mean_value, 2)
        variance = np.mean(squared_diff)
        std_deviation = np.sqrt(variance)
        print("Стандартное отклонение (Моя функция): ",end="")
        return round(std_deviation,2)



