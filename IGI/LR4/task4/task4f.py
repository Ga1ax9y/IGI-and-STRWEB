from abc import ABC,abstractmethod
from math import sin,radians,cos
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


class GeometricFigure(ABC):

    @abstractmethod
    def calculate_area(self):
        pass


class Color():
    def __init__(self,color) -> None:
        self.hidden_color = color


    def get_color(self):
        return self.hidden_color

    def set_color(self, value):
            self.hidden_color = value


    color = property(get_color,set_color)

class MessageMixin:
    def message(self,message):
        print(f"Фигура: {message}")

class Parallelogram(GeometricFigure,MessageMixin):
    name = "Паралеллограмм"
    def __init__(self, diagonal1:float, diagonal2:float, angle:float, col:str):

        self.name = "Паралеллограмм"
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2
        self.angle = angle
        self.color = Color(col)

    def do_something(self):
        self.message("Параллелограмм")

    def __eq__ (self,other):
            return self.calculate_area() == other.calculate_area()
    def __gt__(self, other):
        return self.calculate_area() > other.calculate_area()
    def __lt__(self, other):
        return self.calculate_area() < other.calculate_area()
    def __ge__(self, other):
        return self.calculate_area() >= other.calculate_area()
    def __le__(self, other):
        return self.calculate_area() <= other.calculate_area()

    def get_name(self):
        return self.name

    def set_name(self,name):

        self.name = name



    def calculate_area(self):
        '''Function for calculating area of parallelogram

        '''
        return (self.diagonal1 * self.diagonal2 * sin(radians(self.angle)))/2

    def get_info(self):
        '''Function for getting info about figure

        '''
        area = round(self.calculate_area(),2)
        info = "Параллелограмм {} цвета с диагональю №1 равной {}, диагональю №2 равной {}, уголом между ними {} градусов, площадью {}.".format(self.color.color,self.diagonal1,self.diagonal2,self.angle,area)
        return info

    def draw(self, title):
        '''Function for drawing figure

        keyword argument:
        title -- title(name) of figuree

        '''
        angle_rad = np.radians(self.angle)

        x_A = 0
        y_A = 0

        a = (1/2) * np.sqrt(self.diagonal1**2+self.diagonal2**2 - 2 * self.diagonal1 *self.diagonal2*np.cos(angle_rad))
        b = (1/2) * np.sqrt(self.diagonal1**2+self.diagonal2**2 + 2 * self.diagonal1 *self.diagonal2*np.cos(angle_rad))

        if (self.diagonal1 == self.diagonal2):
            h = a
        else:
            h = round(self.calculate_area(),1) / b

        x_B = np.sqrt(a**2 - h**2)
        y_B = h


        x_D = b
        y_D = 0

        x_C = b + x_B
        y_C = y_B

        x_coords = [x_A, x_B, x_C, x_D, x_A]
        y_coords = [y_A, y_B, y_C, y_D, y_A]

        plt.plot(x_coords, y_coords,color = self.color.color)
        points = [(x_A,y_A),(x_B,y_B),(x_C,y_C),(x_D,y_D)]

        polygon = Polygon(points, closed=True, facecolor=self.color.color, alpha=0.3)
        plt.gca().add_patch(polygon)

        plt.xlabel('X')
        plt.ylabel('Y')
        self.set_name(title)
        plt.title(self.get_name(),color="blue")
        plt.grid(True)
        plt.axis('equal')
        plt.savefig(r'C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task4\plots.png', dpi=300)
        plt.show()
