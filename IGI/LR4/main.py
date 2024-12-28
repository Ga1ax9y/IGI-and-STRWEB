import task1.task1test as task1
import task2.task2test as task2
import task3.task3test as task3
import task4.task4test as task4
import task5.task5test as task5

def main():
    while True:
        while True:
            try:
                choise = input("Выберите номер задания: ")
                if choise!='1' and choise!='2' and choise!='3' and choise!='4' and choise!='5':
                    raise ValueError
                break
            except ValueError:
                print("Ошибка ввода")
        user_func = "task" + choise + "." +"main()"
        eval(user_func)
        restart = input("Хотите продолжить (y/N)?")
        if restart == "N":
            break


if __name__ == "__main__":
    main()
