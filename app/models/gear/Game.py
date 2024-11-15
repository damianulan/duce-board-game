from app.bin.dbengine import *
from app.models.bin.BaseModel import BaseModel
from app.models.Player import Player

class Game(BaseModel):
    id = AutoField()
    instance = IntegerField(default=1)
    turn = IntegerField(default=0)

    @staticmethod
    def factory():
        Game.create()

    @staticmethod
    def migrate():
        db.create_tables([Game])

    @staticmethod
    def rollback():
        db.drop_tables([Game])

    @staticmethod
    def recreate():
        db.drop_tables([Game])
        db.create_tables([Game])
        Game.factory()

    @staticmethod
    def get_instance():
        return Game.get(Game.id == 1)

    @staticmethod
    def get_turn():
        g = Game.get_instance()
        return g.turn

    @staticmethod
    def next_turn():
        g = Game.get_instance()
        g.turn = g.turn + 1
        players = Player.get_active()
        for player in players :
            player.process_turn()
        g.save()
        return g.turn
