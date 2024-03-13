def Multiplication():
    result = 1
    n = int(input())
    while n <= 0:
        result *=n
        n = int(input())
    print("Результат выполнения: ",result)
Multiplication()
