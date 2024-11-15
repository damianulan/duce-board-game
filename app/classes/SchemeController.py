from app.bin.lib import *
from app.models.Player import Player

class SchemeController:
    MURDER = 'murder'
    GOSSIP = 'gossip'
    SECRET = 'secret'
    RELATION = 'relation'
    OBDUCT = 'obduct'

    def makescheme(self, shortname, schemecode, operator):
        player = Player.find(shortname)
        scheme = getattr(self, schemecode)

        if player and scheme :
            match scheme:
                case self.MURDER:
                    if not operator :
                        danger("Nie podano celu operacji")
                        return False
                    return self.murder_scheme(player, operator)
                case _:
                    danger("Nie rozpoznano schematu")


    def murder_scheme(self, player, operator):
        """
        :param Player player:
        :param operator:
        :return:
        """
        base_modifier = 0
        base_modifier += player.scheme_modifier()
        target = Player.find(operator)

        if target :
            target_defense = target.defence_modifier()
            base_modifier -= target_defense


        return True