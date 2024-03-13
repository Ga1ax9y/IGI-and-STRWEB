def Uppercaseletters_find():
    count = 0
    s = input()
    for c in s:
        if c.isupper() or c.isdigit():
            count+=1
    print("Количество больших букв и цифр: ", count)
Uppercaseletters_find()
