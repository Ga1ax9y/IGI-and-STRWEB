from task3.task3f import *
from math import log,pow
import numpy as np
import matplotlib.pyplot as plt

class Drawer():
    def __init__(self,power_series) -> None:
        self.power_series = power_series

    def draw_series(self):
        '''Function for drawing graph

        '''
        #x = np.arange(-100, 100, 0.1)
        #x_m = np.concatenate((np.arange(-100.0, 0, 0.1), np.arange(0, 100.0, 0.1)))
        x1 = np.concatenate((np.arange(-10.0, -1.1, 0.1),np.arange(-1.1, -1.0001, 0.0001)))
        x2 = np.concatenate((np.arange(1.0001, 1.1, 0.0001), np.arange(1.1, 10.0, 0.1)))
        x = np.concatenate((np.arange(-100,0, 0.0001), np.arange(0, 100, 0.1)))
        #x1 = np.linspace(-10, -1, 100, endpoint=False)
        #x2 = np.linspace(10, 1, 100, endpoint=False)
        #x = np.linspace(-10, 10, 100, endpoint=False)

        f1 = np.log((x1+1)/(x1-1))
        f2 = np.log((x2+1)/(x2-1))
        plt.plot(x1, f1,label="math log",color="green",linewidth=2.5)
        plt.plot(x2, f2,color="green",linewidth=2.5)

        con = self.power_series.calculate()
        f3 =  2*sum(1/((2*n+1) * np.power(x,2*n+1)) for n in range(con[1])) #len serie

        #plt.plot(x, f1,label="math log",color="green")
        plt.plot(x, f3,label="my log",color="red",linewidth=1)
        plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
        plt.axvline(x=1, color='blue', linestyle="--", linewidth=1)
        plt.axvline(x=-1, color='blue', linestyle="--", linewidth=1)
        plt.axvline(x=0, color='black', linestyle="-", linewidth=1)

        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        #plt.arrow(0, 0, 3, 4, head_width=0.2, head_length=0.3, fc='blue', ec='blue')
        plt.annotate('Начало координат', xy=(0, 0), xytext=(3, -4),
            arrowprops=dict(facecolor='black', shrink=0.01,width=1))
       # plt.annotate('x >|1|', (2.5, -9))
        plt.title('График функции log((x+1)/(x-1))')
        plt.text(2.5,-7,"green - math log\nred - my log",color='blue')
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.savefig(r'C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task3\plots.png', dpi=300)
        plt.show()
