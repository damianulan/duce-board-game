from app.models.gear.UsedDeck import UsedDeck
from app.bin.lib import *

class DS_1:
    missionname = 'Podwójny Agent'
    player = None
    answer = 'Francesco'
    bribed = False
    bribe_success = False
    bribe_price = 12
    evidenced = False

    def __init__(self, player):
        self.player = player

    def getname(self):
        return self.__class__.__name__

    def intro(self):
        name = self.getname()
        highlight("\n### Misja Służba Księciu ["+name+"]: dla gracza: "+self.player.name()+" ### \n"
              "* "+ self.missionname +" *\n\n"
              "Książę ma silne podejrzenia, że jeden z jego kluczowych doradców jest w zmowie z wrogami spoza dworu. Postanawia powierzyć Tobie przeprowadzenie śledztwa.\n"
              "W tej sprawie poczyniono już wstępne rozpytanie potencjalnych podejrzanych.\n\n"
              "Przyjrzyj się zeznaniom oraz spróbuj odnaleźć dodatkowe dowody [evidence], czy dokonać próby przekupstwa świadków [bribe], aby zdobyć więcej informacji. Następnie wskaż zdrajcę [answer].\n\n"
              "* Doradca Francesco twierdzi, że Antonio odbiera ostatnio sporo podejrzanych listów. Nie udało mu się jednak przechwycić żadnego z nich więc nie ma na to dowodów *\n"
              "* Mateo został już wielokrotnie przyłapany podczas schadzki z dwórką Cateriną. Można spekulować, że to z nią spędza każdy wolny czas. *\n"
              "* Pietro twierdzi, że Antonio ma wielu znajomych poza Księstwem i często wyjeżdża *\n"
              "* Antonio nie potrafi wskazać, kto mógłby się dopuścić zdrady, jednak jest przekonany co do silnej lojalności Pietro. *\n"
              "\n"
              )

    def bribe(self):
        if not self.bribed:
            print("Próba przekupienia świadków.\n")
            r = dice_highest_score(10, self.player.intrigue, 12)
            self.bribed = True
            if r:
                print("Dwórka Caterina zaoferowała swoją pomoc w sprawie. Twierdzi, że jest w posiadaniu kluczowej plotki dla rozwiązania zagadki. Żąda jednak 12 denarów w ramach nagrody.")
                warning("Przystać na tą ofertę? [Y/n]: ")
                yes_no = input()
                if yes_no.lower() == 'y':
                    if self.player.gold >= self.bribe_price :
                        self.bribe_success = True
                        print("# Caterina twierdzi, że Francesco posiada długi w zagranicznej walucie. # \n")
                    else :
                        danger("Nie stać cię na przeprowadzenie tej transakcji. Brakuje " + str(self.bribe_price - self.player.gold) + " denarów.")

            else:
                danger("Próba przekupstwa nieudana. Nie pozyskano nowych informacji.")
        else:
            danger("Próba przekupstwa została już dokonana.")

        return False

    def evidence(self):
        if not self.evidenced:
            self.evidenced = True
            print("Próba szukania nowych dowodów.\n")
            xp_mod = int(self.player.get_xp_modifier())
            chances = binary_chances((xp_mod + self.player.cunning) * 4)
            res = dice_probability(6, chances)
            if res=='yes' :
                print("Udało ci się wejść w posiadanie jednego z listów Antonio, które opisywał Francesco. Każde z nich jest listem miłosnym od jednej z dworek. Bez powiązania ze sprawą.")
            else :
                danger("Nie udało się odnaleźć nowych dowodów.")

        else:
            danger("Próba znalezienia nowych dowodów została już podjęta.")

        return False

    def try_answer(self, response):
        if self.answer.lower() == response.strip().lower():
            success("Gratulacje! Zagadka rozwiązana poprawnie.")
            self.reward()
        else :
            danger("Francesco następnego dnia ucieka z dworu do swoich mocodawców. Książę obwinia cię za ukaranie lojalnego doradcy.")
            self.punishment()
        if self.bribe_success :
            self.player.remove_gold(30)

        return True

    def reward(self):
        self.player.add_influence(5)
        self.player.add_gold(10)
        self.player.add_xp(5)
        self.player.modify_relations('duce', 5)
        success("# W nagrodę otrzymałeś PW15 oraz 30 denarów. #")

    def punishment(self):
        self.player.remove_influence(4)
        self.player.add_xp(2)
        self.player.modify_relations('duce', -3)
        danger("# Tracisz PW10! #")

    def interpreter(self, command):
        match command.lower().strip():
            case "bribe":
                return self.bribe()
            case "evidence":
                return self.evidence()
            case "skip":
                print("Misja pominięta. Możesz do niej wrócić poprzez polecenie action [id_gracza] [id_misji]")
                return True
            case "answer":
                resp = ''
                while resp.strip() == '':
                    resp = input("Podaj odpowiedź [Ta operacja jest nieodwracalna]: ")
                return self.try_answer(resp)
            case _:
                return False

    def launch(self):
        self.player.add_task(self.getname())
        UsedDeck.mark_card(self.getname())
        self.intro()
        result = False
        while not result:
            command = input()
            result = self.interpreter(command)

        return True