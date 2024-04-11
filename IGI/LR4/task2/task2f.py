import re
from collections import Counter

class TextAnalyzer():

    @classmethod
    def find_sentences(self,text: str) ->str:
        pattern = r'[^.!?]*[.!?]+'
        sentences = re.findall(pattern, text)
        output = "Количество предложений: "
        output += str(len(sentences))
        output +="\n"
        return output

    @classmethod
    def find_sentences_bytype(self, text:str) ->None:
        pattern_narrative = r'[^.!?]*[.]+'
        pattern_interrogative = r'[^.!?]*[?]+'
        pattern_imperative = r'[^.!?]*[!]+'

        sentences_narrative = re.findall(pattern_narrative, text)
        sentences_quest = re.findall(pattern_interrogative, text)
        sentences_imperative = re.findall(pattern_imperative, text)
        output = ""
        output += "Количество повествовательных предложений: "
        output += str(len(sentences_narrative))
        output += "\n"
        output += "Количество вопросительных предложений: "
        output += str(len(sentences_quest))
        output += "\n"
        output += "Количество вопросительных предложений: "
        output += str(len(sentences_imperative))
        output += "\n"
        return output

    @classmethod
    def avg_sentence(self, text:str) ->str:
        pattern = r'[^.!?]*[.!?]+'
        sentences = re.findall(pattern, text)

        total_sentences = len(sentences)
        total_char_count = 0

        for sentence in sentences:
            punct_pattern = r'[^\w\s]'
            sentence_without_punctuation = re.sub(punct_pattern, '', sentence)
            words = sentence_without_punctuation.split()

            char_count = sum(len(word) for word in words)
            total_char_count += char_count

        output = ""
        output += "Cредняя длина предложения в символах: "
        output += str(total_char_count / total_sentences)
        output += "\n"
        return output

    @classmethod
    def avg_word(self, text:str) -> str:
        punct_pattern = r'[^\w\s]'
        text_without_punc = re.sub(punct_pattern, '', text)

        words = text_without_punc.split()
        total_char_count = sum(len(word) for word in words)
        total_word_count = len(words)

        output = ""
        output += "Cредняя длина слова в тексте в символах: "
        output += str(total_char_count / total_word_count)
        output += "\n"
        return output

    @classmethod
    def smile_count(self,text:str) -> str:
        pattern = r'(?<![:;])[;:]-*(?:\[+|\]+|\)+|\(+)'
        smileys = re.findall(pattern, text)
        count = 0
        count = len(smileys)

        output = "Количество смайликов: "
        output += str(count)
        output += "\n"
        return output

    @classmethod
    def phone_number(self,text:str) -> str:
        pattern = r'\b29\d{7}\b'
        phone_numbers = re.findall(pattern, text)

        output = "Телефонные номера: "
        for num in phone_numbers:
            output += str(num)
            output += " "
        output += "\n"
        return output

    @classmethod
    def vowel(self,text:str) -> str:
         pattern = r'\b\w[bcdfghjklmnpqrstvwxyz][aeiou]\w*\b'
         words = re.findall(pattern, text, re.IGNORECASE)

         output = "Слова, у которых вторая буква согласная, а третья – гласная: "
         for word in words:
             output += word
             output += " "
         output += "\n"
         return output

    @classmethod
    def space_word(self, text:str) -> str:
        pattern = r'\b[A-Za-zА]+\b'
        words = re.findall(pattern, text)
        default_words = text.split()
        count = 0
        for i in range(len(words)-1):
            if words[i] == default_words[i]:
                count+=1

        output = "Число слов, ограниченных пробелами: "
        output += str(count)
        output += "\n"
        return output


    @classmethod
    def count_letter_occurrences(self,text:str):
        punct_pattern = r'[^\w\s]'
        text_without_punc = re.sub(punct_pattern, '', text)
        text_without_punc = text_without_punc.replace(" ", "")

        letter_counts = Counter(text_without_punc).most_common()
        output = "Сколько раз повторяется каждая буква: "
        output += str(letter_counts)
        output += "\n"
        return output

    @classmethod
    def alpha_sort(self,text:str) -> str:
        pattern = r'(?<=,)\s*([^,]+)\s*(?=,)'
        words_between_commas = re.findall(pattern, text)
        sorted_words = sorted(words_between_commas)

        output = "Словосочетания, отделенные запятыми по алфавиту: "
        for word in sorted_words:
            output += word
            output += ", "
        output += "\n"
        return output


