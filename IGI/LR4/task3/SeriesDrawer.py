from task3.task3f import *
from math import log,pow
import numpy as np
import matplotlib.pyplot as plt

class Drawer():
    def __init__(self,power_series) -> None:
        self.power_series = power_series

    def draw_series(self):
        x = np.concatenate((np.arange(-100, 1, 0.1), np.arange(1.0000001, 100, 0.1)))
        f1 = np.log((x+1)/(x-1))
        plt.plot(x, f1,label="math log",color="green")

        con = self.power_series.calculate()
        f2 =  2*sum(1/((2*n+1) * np.power(x,2*n+1)) for n in range(100))
        plt.plot(x, f2,label="my log",color="blue")
        plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
        plt.axvline(x=1, color='red', linestyle="--", linewidth=1)
        plt.axvline(x=-1, color='red', linestyle="--", linewidth=1)

        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.annotate('x >|1|', (2.5, -9))
        plt.title('График функции log((x+1)/(x-1))')
        plt.text(2.5,-7,"green - math log\nblue - my log")
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.savefig(r'C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task3\plots.png', dpi=300)
        plt.show()
