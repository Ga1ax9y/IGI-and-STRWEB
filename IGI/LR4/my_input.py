input_error = "Ошибка ввода! Повторите попытку"
def check_error(text):
    while True:
        try:
            value = float(input(text))
            return value
            break
        except ValueError:
            print(input_error)


def check_error_int(text):
    while True:
        try:
            value = int(input(text))
            return value
            break
        except ValueError:
            print(input_error)
