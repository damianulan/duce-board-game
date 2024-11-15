from app.bin.lib import *
from app.models.gear.UsedDeck import UsedDeck
from app.classes.decks.DuceService.autoload import *
import random

class ActionController:

    @staticmethod
    def distribute(player):

        mincode = 0
        maxcode = 0

        match player.location:
            case "throneroom":
                code = 'DS_'
                mincode = 1
                maxcode = 3
            case _:
                code = ''
        if mincode > 0 and maxcode > 0 and code != '':
            tuplelist = list(range(mincode, maxcode))

            is_used = True
            fullcode = None
            proceed = True

            while is_used:
                if not tuplelist :
                    proceed = False
                    break

                randcode = random.choice(tuplelist)
                fullcode = code + str(randcode)
                is_used = UsedDeck.is_deck_used(fullcode)
                if is_used :
                    tuplelist.remove(randcode)

            if fullcode and proceed:
                instance = globals()[fullcode](player)
                return instance.launch()
            else :
                danger("Brak nowych kart w talii.")

        else:
            danger("Nie rozpoznano gracza lub wskazanej lokacji,\n")

        return False
