from app.models.gear.UsedDeck import UsedDeck
from app.bin.lib import *

class DS_2:
    missionname = 'Zagadka Starodawnej Monety'
    player = None
    answers = ['rzym', 'imperium rzymskie', 'cesarstwo rzymskie', 'starożytny rzym', 'rzymska sestercja', ]
    approaches = 0
    base_chance = 0
    A_used = False
    B_used = False
    C_used = False
    D_used = False

    def __init__(self, player):
        self.player = player

    def getname(self):
        return self.__class__.__name__

    def intro(self):
        name = self.getname()
        highlight("\n### Misja Służba Księciu ["+name+"]: dla gracza: "+self.player.name()+" ### \n"
              "* "+ self.missionname +" *\n\n"
              "W swoim rodzinnym skarbcu Książę odnalazł dziwną starodawną złotą monetę. Przekazuje tobie określenie cywilizacji jej pochodzenia. Twierdzi iż pamięta, że jego dziadek miał pewną obsesję na jej punkcie i cały czas nosił ją przy sobie.\n"
              "Odpowiedź podaj za pomocą polecenia [answer].\n"
              "Istnieje kilka różnych podejść do tego zadania.\n\n"
              "# [A]: Przeprowadzenie analizy strukturalnej i historycznej analizy monety \n"
              "# [B]: Przepytanie dawnych rzemieślników z cechu \n"
              "# [C]: Przeszukanie ksiąg w archiwach książęcych \n"
              "# [D]: Poproś o pomoc książęcego skarbnika \n"
              "\n"
              )

    def A(self):
        if self.A_used:
            print("Ta opcja została już wykorzystana.")
            return False
        if self.approaches > 2:
            print("Wszystkie możliwe opcje zostały wyczerpane. Podaj odpowiedź [answer].")
            return False
        base = 80 + self.base_chance
        result = dice_binary(base)
        if result :
            print("")
        else :
            print("Ciężko było ustalić jakieś znaki szczególne, moneta jest stara i przetarta. Na awersie na pewno widnieje profil jakieś osoby.")

        self.base_chance += 5
        self.A_used = True
        return False

    def B(self):
        if self.B_used:
            print("Ta opcja została już wykorzystana.")
            return False
        if self.approaches > 2:
            print("Wszystkie możliwe opcje zostały wyczerpane. Podaj odpowiedź [answer].")
            return False
        base = 10 + self.base_chance
        result = dice_binary(base)
        if result:
            print("")
        else:
            print("")

        self.base_chance += 5
        self.B_used = True
        return False

    def C(self):
        if self.C_used:
            print("Ta opcja została już wykorzystana.")
            return False
        if self.approaches > 2:
            print("Wszystkie możliwe opcje zostały wyczerpane. Podaj odpowiedź [answer].")
            return False
        base = 10 + self.base_chance
        result = dice_binary(base)
        if result:
            print("")
        else:
            print("")

        self.base_chance += 5
        self.C_used = True
        return False

    def D(self):
        if self.D_used:
            print("Ta opcja została już wykorzystana.")
            return False
        if self.approaches > 2:
            print("Wszystkie możliwe opcje zostały wyczerpane. Podaj odpowiedź [answer].")
            return False
        base = 70 + self.base_chance
        base += self.player.get_relation('steward')
        result = dice_binary(base)
        if result:
            print("")
        else:
            print("")

        self.base_chance += 5
        self.D_used = True
        return False

    def try_answer(self, response):
        if response.strip().lower() in self.answers:
            success("Gratulacje! Zagadka rozwiązana poprawnie.")
            self.reward()
        else :
            danger("Francesco następnego dnia ucieka z dworu do swoich mocodawców. Książę obwinia cię za ukaranie lojalnego doradcy.")
            self.punishment()

        return True

    def reward(self):
        self.player.add_influence(5)
        self.player.add_gold(10)
        self.player.add_xp(5)
        self.player.modify_relations('duce', 3)
        success("# W nagrodę otrzymałeś PW15 oraz 30 denarów. #")

    def punishment(self):
        self.player.remove_influence(4)
        self.player.add_xp(2)
        self.player.modify_relations('duce', -2)
        danger("# Tracisz PW10! #")

    def interpreter(self, command):
        match command.lower().strip():
            case "a":
                return self.A()
            case "b":
                return self.B()
            case "c":
                return self.C()
            case "d":
                return self.D()
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