def Symbols_remove(str):
    symbols_to_remove = ",!?."
    for symbol in symbols_to_remove:
        str = str.replace(symbol,"")
    return str

def Words_count(str):
    str = Symbols_remove(str)
    words = str.split()
    print(len(words))

def Longest_word(str):
    str = Symbols_remove(str)
    count=1
    max_count = 1
    Max_word = ""
    words = str.split()
    for word in words:
        if len(word) > len(Max_word):
            Max_word = word
            max_count = count
        count+=1
    print(Max_word,max_count)

def NotEvenWords(str):
    str = Symbols_remove(str)
    words = str.split()
    print(*words[::2])


def StringWork():
    s = '''So she was considering in her own mind,
 as well as she could, for the hot day made her feel very sleepy and stupid,
 whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies,
 when suddenly a White Rabbit with pink eyes ran close by her. '''
    Words_count(s)
    Longest_word(s)
    NotEvenWords(s)
StringWork()
