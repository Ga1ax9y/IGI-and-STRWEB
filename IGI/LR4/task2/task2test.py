from task2.task2f import *
from task2.fileworker import *


def main():

    filenamer = r".\task2\string_from_file.txt"
    filenamew = r".\task2\file_from.txt"

    File_work = ZipWorker()
    
    text = File_work.read_from_file(filenamer)

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

    File_work.write_to_file(filenamew,text_output)

    File_work.archive_file(filenamer,filenamew)

if __name__ == "__main__":
    main()
