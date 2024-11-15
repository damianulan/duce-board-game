from app.bin.dbengine import *
from app.models.bin.BaseModel import BaseModel
from app.models.Player import Player
from app.bin.engine import LOCATIONS
from app.models.gear.Game import Game
from app.bin.lib import lang
from app.classes.ActionController import *

class Move(BaseModel):
    id = AutoField()
    player = ForeignKeyField(Player, backref='movements')
    prev_location = CharField()
    new_location = CharField()
    action_type = CharField()
    turn = IntegerField(default=1)

    @staticmethod
    def migrate():
        db.create_tables([Move])

    @staticmethod
    def rollback():
        db.drop_tables([Move])

    @staticmethod
    def recreate():
        db.drop_tables([Move])
        db.create_tables([Move])

    @staticmethod
    def move_to(shortname, location):
        player = Player.find(shortname)
        game = Game.get_instance()
        if player and game and location in LOCATIONS and player.location != location:
            Move.create(player=player.id,prev_location=player.location,new_location=location,action_type='change_location',turn=game.turn)
            player.location = location
            player.save()
            print("Gracz "+ lang('character.'+shortname) + " przenosi się do nowej lokacji: "+ lang('location.'+location) + ".")

            return True

        if location not in LOCATIONS:
            print("Nie jest możliwe udanie się do następującej lokacji: "+location)

        if location == player.location:
            print("Gracz już znajduje się we wskazanej lokacji.")
        return False

    @staticmethod
    def make_action(shortname, taskcode):
        player = Player.find(shortname)
        game = Game.get_instance()

        if player and game:

            if taskcode :
                has_task = player.get_task(taskcode)
                if has_task :
                    instance = globals()[taskcode](player)
                    return instance.launch()

                else :
                    print("Gracz nie ma przypisanej karty z tym zadaniem.")
            else :
                if player.can_take_actions():
                    moves = list(Move.select().where(Move.turn==game.turn, Move.action_type=='location_action', Move.player==player.id).execute())

                    if len(moves) == 0:
                        result = ActionController.distribute(player)
                        if result :
                            Move.create(player=player.id, prev_location=player.location, new_location=player.location,
                                        action_type='location_action', turn=game.turn)

                        return result
                    else :
                        print(lang('character.'+shortname)+" ma już wykorzystane akcje w tej turze.")

        return False