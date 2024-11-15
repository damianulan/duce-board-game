from app.bin.dbengine import *
from app.bin.engine import *
from app.models.bin.BaseModel import BaseModel
from app.models.Player import Player

class UsedDeck(BaseModel):
    id = AutoField()
    codename = CharField()

    @staticmethod
    def mark_card(code):
        if not UsedDeck.is_deck_used(code):
            UsedDeck.create(codename=code)
        return True

    @staticmethod
    def is_deck_used(code):
        result = list(UsedDeck.select().where(UsedDeck.codename == code).execute())
        return len(result) > 0

    @staticmethod
    def migrate():
        db.create_tables([UsedDeck])

    @staticmethod
    def rollback():
        db.drop_tables([UsedDeck])

    @staticmethod
    def recreate():
        db.drop_tables([UsedDeck])
        db.create_tables([UsedDeck])