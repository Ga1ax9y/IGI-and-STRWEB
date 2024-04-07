import string
uppercase_letters = string.ascii_uppercase

def Uppercaseletters_find(s):
    """Function for counting the number of uppercase letters and numbers

    Keyword argument:
    s -- string

    Return value:
    count -- amount of uppercase letters and numbers

    """
    count = 0
    for c in s:
        if c in uppercase_letters or c.isdigit():
            count+=1
    return count


