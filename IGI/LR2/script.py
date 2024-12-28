import os
import square
import circle

#shape = os.environ.get("SHAPE")
#action = os.environ.get("ACTION")
size = float(os.environ.get("SIZE"))
shape = input()
action = input()

funcs = {
    ("circle","area"): circle.area,
    ("circle","perimeter"): circle.perimeter,
    ("square","area"): square.area,
    ("circle","perimeter"): square.perimeter
}
func = funcs.get((shape,action))
print("Result",func(size))
