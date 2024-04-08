from task1f import * #######

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
    with open("CsvSer.csv","w",encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh,quoting=csv.QUOTE_ALL)
        writer.writerow(["Кандидат", "Количество голосов"])
        for name,votes in sorted(elec.candidates.items(),key= lambda x: x[1],reverse=True):
            writer.writerow([name,votes])

    rows = []
    with open("CsvSer.csv","r",encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    for row in rows:
        print(row)

    #2 способ
    filename = "PickleSer.txt"
    with open(filename,"wb") as fh:
        pickle.dump(sorted(elec.candidates.items(),key= lambda x: x[1],reverse=True),fh)
    des_candidates = []

    with open(filename,"rb") as fh:
        des_candidates = pickle.load(fh)
    print(des_candidates)


if __name__ == "__main__":
    main()
