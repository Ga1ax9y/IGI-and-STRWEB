from math import pow,log
import numpy as np
import statistics as st

class SeriesName():
    def __init__(self,name) -> None:
        self.name = name

class PowerSeries(SeriesName):
    def __init__(self, x, eps) -> None:
        super().__init__("PowerSeries")
        self.x = x
        self.eps = eps
        self.serie = []

    def calculate(self):
        n=0
        result = 0.0
        final_result = 0.0
        sum = 2/((2*n+1)*pow(self.x,2*n+1))
        while abs(sum) >= self.eps:
            result = sum
            self.serie.append(result)
            final_result += result
            n+=1
            sum = 2/((2*n+1)*pow(self.x,2*n+1))

            if n > 500:
                print("Больше 500")
                break
        return (final_result, n+1)

    def get_metrics(self):
        print("Среднее значение элементов: ", np.mean(self.serie))
        print("Медиана: ",np.median(self.serie))
        print("Мода:", st.mode(self.serie))
        print("Дисперсия: ", np.var(self.serie))
        print("СКО: ",np.std(self.serie))

    def get_serie(self):
        return self.serie
