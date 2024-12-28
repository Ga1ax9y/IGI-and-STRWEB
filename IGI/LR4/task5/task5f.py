import numpy as np



class NumpyBasic():
    @classmethod
    def create_matrix(self, n, m, max_value):
        '''Function for creating matrix

        keyword argument:
        n -- rows
        m -- columns
        max_value -- max value of matrics

        return value:
        arr -- matrix
        '''
        if n > 0 and m > 0:
            rng = np.random.default_rng()
            arr =rng.integers(max_value,size=(n,m))
            return arr
        else:
            raise ValueError

    @classmethod
    def create_array(self, n, m, size):
        '''Function for creating array

        keyword argument:
        n -- min value
        m -- max value
        size -- size of array

        return value:
        arr -- array
        '''
        if size > 0 :
            arr = np.random.randint(n,m,size)
            return arr
        else:
            raise ValueError

    @classmethod
    def index_array(self, your_arr, index):
        '''Function for getting element by index

        keyword argument:
        your_arr -- array
        index -- index of element

        return value:
        your_arr[index] -- value of elemnt with index
        '''
        if -(len(your_arr)) <=index <= len(your_arr)-1:
            print("Исходный массив: ",your_arr)
            print(f"Элемент номер {index}: ",end="")
            return your_arr[index]
        else:
            raise ValueError


    @classmethod
    def slice_array(self, your_arr, start, end, step = 1)->np.array:
        '''Function for slicing array

        keyword argument:
        your_arr -- array
        start -- first index
        end -- last index
        step -- step

        return value:
        your_arr[start:end:step] -- sliced array
        '''
        print("Исходный массив: ",your_arr)
        if (0 <= start <= len(your_arr)) and (0 <= end <= len(your_arr)):
            print(f"Срез от [{start},{end}) с шагом: {step}: ",end="" )
            return your_arr[start:end:step]
        else:
            raise ValueError

    @classmethod
    def sum_2_arrays(self, arr1, arr2):
        '''Function for sum of 2 arrays

        keyword argument:
        arr1 -- first array
        arr2 -- second array

        return value:
        np.add(arr1,arr2) -- sum of 2 arrays
        '''
        print("Сумма двух массивов: ")
        return np.add(arr1,arr2)

    @classmethod
    def power_array(self, arr, power):
        '''Function for power of array

        keyword argument:
        arr -- array
        power -- power

        return value:
        np.power(arr,power) -- power of array
        '''
        print(f"Массив в степени {power}: ",end="")
        return np.power(arr,power)

    @classmethod
    def sin_of_array(self, arr):
        '''Function for sinus of array

        keyword argument:
        arr -- array

        return value:
        np.sin(arr) -- sinus of array
        '''
        print("Синусы массива: ",end="")
        return np.sin(arr)

    @classmethod
    def sqrt_of_array(self, arr):
        '''Function for sqrt of array

        keyword argument:
        arr -- array

        return value:
        np.sqrt(arr) -- sqrt of array
        '''
        print("Корень из массива: ",end="")
        return np.sqrt(arr)

    @classmethod
    def array_mean(self, arr):
        '''Function for finding the average value of the array elements

        keyword argument:
        arr -- array

        return value:
        np.mean(arr) -- the average value of the array elements
        '''
        print("Среднее значение элементов массива: ", end="")
        return np.mean(arr)

    @classmethod
    def array_median(self, arr):
        '''Function for finding the median of the array elements

        keyword argument:
        arr -- array

        return value:
        np.median(arr) -- median of the array elements
        '''
        print("Медиана массива: ",end="")
        return np.median(arr)

    @classmethod
    def array_corr(self,arr1,arr2):
        '''Function for finding correlation coefficient

        keyword argument:
        arr1 -- first array
        arr2 -- second array

        return value:
        np.corrcoef(arr1,arr2) -- correlation coefficient
        '''
        print("Коэффициент корреляции: ",end="")
        return np.corrcoef(arr1,arr2)

    @classmethod
    def arrray_variance(self,arr):
        '''Function for finding the variance of the array elements

        keyword argument:
        arr -- array

        return value:
        np.var(arr) -- variance of the array elements
        '''
        print("Дисперсия массива: ", end="")
        return np.var(arr)


class NumpyResearch(NumpyBasic):

    @classmethod
    def array_std(self,arr):
        '''Function for finding the Standard deviation

        keyword argument:
        arr -- array

        return value:
        np.std(arr) -- Standard deviation
        '''
        print("Стандартное отклонение (numpy): ",end="")
        return np.std(arr)

    @classmethod
    def sum_neg_odd(self,arr):
        '''Function for finding The sum of the modules of negative odd elements

        keyword argument:
        arr -- array

        return value:
        sum_of_abs -- The sum of the modules of negative odd elements
        '''
        neg_odd_elements = arr[(arr < 0 ) & (arr % 2 !=0)]
        sum_of_abs = np.sum(np.abs(neg_odd_elements))
        print("Cумма модулей отрицательных нечетных элементов: ",end="")
        return sum_of_abs

    @classmethod
    def my_array_std(self,arr):
        ''' My function for finding The sum of the modules of negative odd elements

        keyword argument:
        arr -- array

        return value:
        ound(std_deviation,2) -- The sum of the modules of negative odd elements
        '''
        mean_value = np.mean(arr)
        squared_diff = np.power(arr - mean_value, 2)
        variance = np.mean(squared_diff)
        std_deviation = np.sqrt(variance)
        print("Стандартное отклонение (Моя функция): ",end="")
        return round(std_deviation,2)
