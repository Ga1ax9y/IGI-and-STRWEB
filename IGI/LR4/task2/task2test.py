from task2.task2f import *
import zipfile

def main():
    filenamer = r"C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task2\string_from_file.txt"
    filenamew = r"C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task2\file_from.txt"

    with open(filenamer,"r",encoding="utf-8") as file:
        text = file.read()

    text_output = ""
    text_output += TextAnalyzer.find_sentences(text)
    print(TextAnalyzer.find_sentences(text))

    text_output += TextAnalyzer.find_sentences_bytype(text)
    print(TextAnalyzer.find_sentences_bytype(text))

    text_output += TextAnalyzer.avg_sentence(text)
    print(TextAnalyzer.avg_sentence(text))

    text_output += TextAnalyzer.avg_word(text)
    print(TextAnalyzer.avg_word(text))

    text_output += TextAnalyzer.smile_count(text)
    print(TextAnalyzer.smile_count(text))

    text_output += TextAnalyzer.phone_number(text)
    print(TextAnalyzer.phone_number(text))

    text_output += TextAnalyzer.vowel(text)
    print(TextAnalyzer.vowel(text))

    text_output += TextAnalyzer.space_word(text)
    print(TextAnalyzer.space_word(text))

    text_output += TextAnalyzer.count_letter_occurrences(text)
    print(TextAnalyzer.count_letter_occurrences(text))

    text_output += TextAnalyzer.alpha_sort(text)
    print(TextAnalyzer.alpha_sort(text))

    with open(filenamew, "w",encoding="utf-8") as file:
        file.write(text_output)

    with zipfile.ZipFile(r'C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task2\Task2_archive.zip', 'w') as zip_ref:
        zip_ref.write(filenamer)
        zip_ref.write(filenamew)

if __name__ == "__main__":
    main()
