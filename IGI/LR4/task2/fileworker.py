import zipfile
from abc import abstractmethod,ABC

class IFileWorker(ABC):

    def read_from_file(self, path:str):
        '''Function for reading from file

        Keyword argument:
        path -- path to file

        Retuen value:
        text -- text from file

        '''
        try:
            with open(path,"r",encoding="utf-8") as file:
                text = file.read()
            return text
        except Exception:
            print("Ошибка открытия файла")

    def write_to_file(self, path:str, text_output:str):
        '''Function for writing in file

        Keyword arguments:
        path -- path to file
        text_output -- your text

        '''
        try:
            with open(path, "w",encoding="utf-8") as file:
                file.write(text_output)
        except Exception:
            print("Ошибка открытия файла")

    @abstractmethod
    def archive_file():
        pass


class ZipWorker(IFileWorker):

    def archive_file(self,path1:str, path2:str):
        '''Function for archiving file to zip

        Keyword argument:
        path1 -- first file
        path2 -- second file

        '''
        with zipfile.ZipFile(r'.\task2\Task2_archive.zip', 'w') as zip_ref:
            zip_ref.write(path1)
            zip_ref.write(path2)
