

class Elections():

    electioin_country = "Belarus"

    def __init__(self, candidates= {}) -> None:
        self.availiable_voters = 2000
        self.__check_votes(candidates)
        self.candidates = candidates



    def __check_votes(self,candidates):
        votes = 0
        for name in candidates:
            votes += candidates[name]
        if votes >=0:
            self.candidates = candidates
            self.availiable_voters -= votes
        else:
            raise ValueError



    def add_candidate(self,last_name,votes) -> None:
        if self.availiable_voters - votes >=0:
            self.candidates[last_name] = votes
            self.availiable_voters -=votes
        else:
            raise ValueError

    def print_info_about(self,last_name) -> None:
        if last_name in self.candidates:
            print("Информация о кандидате")
            print("======================")
            print(f"Фамилия: {last_name}\nКоличество голосов за: {self.candidates[last_name]}")
            print("======================")
        else:
            print(f"Кандидат {last_name} не найден!")

    def sort_by_votes(self) -> None:
        sorted_results = sorted(self.candidates.items(),key= lambda x: x[1],reverse=True)
        print("======================")
        print("Результаты выборов")
        print("======================")
        for candidate, votes in sorted_results:
            print(candidate, votes)
        print("======================")

    def status(self) -> None:
        total_votes = 2000
        limit = total_votes / 3
        passed_candidates = []

        for candidate,votes in self.candidates.items():
            if votes >= limit:
                print(f"Кандидат {candidate} прошел!")
                passed_candidates.append(candidate)
            else:
                print(f"Кандидат {candidate} не прошел!")
        if len(passed_candidates) == 0:
            print("Необходимо провести повторные выборы!")
