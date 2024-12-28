def symbols_remove(str):
    """Function for removing punctuation marks

    Keyword argument:
    str -- string

    Return value:
    str -- formatted string

    """
    symbols_to_remove = ",!?."
    for symbol in symbols_to_remove:
        str = str.replace(symbol,"")
    return str

def words_count(str):
    """Function for counting the number of words

    Keyword argument:
    str -- string

    Return value:
    amount -- the number of words in string

    """
    str = symbols_remove(str)
    words = str.split()
    amount = len(words)
    return amount

def longest_word(str):
    """Function for determining the longest word

    Keyword argument:
    str -- string

    Return values:
    max_word -- the longest word
    max_count -- the position of the longest word

    """
    str = symbols_remove(str)
    count=1
    max_count = 1
    max_word = ""
    words = str.split()
    for word in words:
        if len(word) > len(max_word):
            max_word = word
            max_count = count
        count+=1
    return (max_word,max_count)

def notEvenWords(str):
    """Function for displaying odd words of a string

    Keyword argument:
    str -- string

    Return value:
    odd_words - list off odd words in the string

    """
    str = symbols_remove(str)
    words = str.split()
    odd_words = words[::2]
    return odd_words
