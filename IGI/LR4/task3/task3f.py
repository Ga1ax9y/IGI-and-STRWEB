from math import pow,log
import numpy as np
import statistics as st


class PowerSeriesStandart():
    def __init__(self, x, eps) -> None:
        self.x = x
        self.eps = eps
        self.serie = []

    def calculate(self):
        '''Function for calculating power series

        Return value:
        final_result -- value of our function
        n - iteration

        '''
        n=0
        result = 0.0
        final_result = 0.0
        sum = 2/((2*n+1)*pow(self.x,2*n+1))
        self.serie.append(sum)
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



class PowerSeriesExtended(PowerSeriesStandart):
    def __init__(self,x,eps):
        super().__init__(x,eps)

    def get_metrics(self):
        '''Function for metrics output

        '''
        print("Среднее значение элементов: ", np.mean(self.serie))
        print("Медиана: ",np.median(self.serie))
        print("Мода:", st.mode(self.serie))
        print("Дисперсия: ", np.var(self.serie))
        print("СКО: ",np.std(self.serie))

    def get_serie(self):
        return self.serie
