from app.bin.lib import *

class TraitController:

    @staticmethod
    def draw_trait(player, traitcode, percent_chance):

        result = binary_probability(percent_chance)
        if result :
            player.add_trait(traitcode)
            return True
        return False