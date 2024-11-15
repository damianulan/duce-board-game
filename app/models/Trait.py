from app.bin.dbengine import *
from app.models.bin.BaseModel import BaseModel

class Trait(BaseModel):
    BOOKWORM = 'bookworm'
    PRISONBREAK = 'prisonbreak'
    ASSASSIN = 'assassin'
    ELDER = 'elder'
    PUPPETEER = 'puppeteer'
    SPY = 'spy'
    GENIUS = 'genius'
    ADEPT = 'adept'
    FOX = 'fox'
    RESILIENT = 'resilient'

    id = AutoField()
    player = IntegerField()
    traitcode = CharField()

    @staticmethod
    def migrate():
        db.create_tables([Trait])

    @staticmethod
    def rollback():
        db.drop_tables([Trait])

    @staticmethod
    def recreate():
        db.drop_tables([Trait])
        db.create_tables([Trait])