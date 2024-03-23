from task4.task4 import *


def main():
    s = '''So she was considering in her own mind,
 as well as she could, for the hot day made her feel very sleepy and stupid,
 whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies,
 when suddenly a White Rabbit with pink eyes ran close by her. '''

    print(f"Количество слов в строке: {words_count(s)}")
    res = longest_word(s)
    print(f"Самое длинное слово - {res[0]} с порядковым номером {res[1]}")
    print("Каждое нечетное слово:")
    odd_words = notEvenWords(s)
    print(*odd_words)


if __name__ == "__main__":
    main()
