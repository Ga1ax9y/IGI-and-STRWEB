def Uppercaseletters_find(s):
    """Function for counting the number of uppercase letters and numbers

    Keyword argument:
    s -- string

    Return value:
    count -- amount of uppercase letters and numbers

    """
    count = 0
    for c in s:
        if c.isupper() or c.isdigit():
            count+=1
    return count

def main():
    s = input("Введите строку: ")
    result = Uppercaseletters_find(s)
    print(f"Количество заглавных букв и цифр: {result}")


if __name__ == "__main__":
    main()
