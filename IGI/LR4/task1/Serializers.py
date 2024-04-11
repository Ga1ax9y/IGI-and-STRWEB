from abc import ABC,abstractmethod
import pickle
import csv

class ISerializer(ABC):
    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def unserialize(self):
        pass

class CsvSerializer(ISerializer):
    def serialize(self,elec):
        with open(r"C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task1\CsvSer.csv","w",encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh,quoting=csv.QUOTE_ALL)
            writer.writerow(["Кандидат", "Количество голосов"])
            for name,votes in sorted(elec.candidates.items(),key= lambda x: x[1],reverse=True):
                writer.writerow([name,votes])
    def unserialize(self):
        rows = []
        with open(r"C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task1\CsvSer.csv","r",encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
        for row in rows:
                print(row)

class TxtSerializer(ISerializer):
    def serialize(self,elec):
        with open(r"C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task1\PickleSer.txt","wb") as fh:
            pickle.dump(sorted(elec.candidates.items(),key= lambda x: x[1],reverse=True),fh)

    def unserialize(self):
        des_candidates = []
        with open(r"C:\Users\Alexander\Desktop\bsuir\IGI\253505_Stanishewski_21\IGI\LR4\task1\PickleSer.txt","rb") as fh:
            des_candidates = pickle.load(fh)
        print(des_candidates)
