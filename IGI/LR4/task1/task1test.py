from task1.task1f import * #######
from task1.Serializers import *
def main():
    elec = Elections()
    print("1.Добавить кандидатов самостоятельно\n2.Использовать готовых\nВыберите вариант: ",end="")
    while(True):
        try:
            choise = int(input())
            if choise !=1 and choise !=2:
                raise ValueError
            break
        except ValueError:
            print("Ошибка ввода!")
    if choise == 1:
        while elec.availiable_voters !=0:
            while True:
                print(f"Доступные голоса: {elec.availiable_voters}")
                candidate_name = input("Введите имя кандидата: ")
                try:
                    votes = int(input("Введите количество голосов за: "))
                    if votes <=0:
                        raise ValueError
                    elec.add_candidate(candidate_name,votes)
                    break
                except ValueError:
                    print("Ошибка ввода")

    elif choise == 2:
        list_of_candidates = {"Дон":100,"Сол Гудман":500,"Джон Сноу":675,"Мистер Вайт":725}
        elec = Elections(list_of_candidates)

    print("1.Посмотреть итоги\n2.Сортировать результаты по возрастанию\n3.Вывести информацию о кандидате\nВыберите вариант: ",end="")
    while(True):
        try:
            choise = int(input())
            if choise !=1 and choise !=2 and choise !=3:
                raise ValueError
            break
        except ValueError:
            print("Ошибка ввода!")
    if choise == 1:
        elec.status()
    elif choise == 2:
        elec.sort_by_votes()
    elif choise == 3:
        choose_person = input("Введите имя кандидата: ")
        elec.print_info_about(choose_person)

    #Сериализация
    #1 способ
    first_ser = CsvSerializer()

    first_ser.serialize(elec)
    first_ser.unserialize()

    #2 способ
    second_ser = TxtSerializer()

    second_ser.serialize(elec)
    second_ser.unserialize()



if __name__ == "__main__":
    main()
