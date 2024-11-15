from app.bin.dbengine import *
from app.bin.engine import *
from app.models.bin.BaseModel import BaseModel
from app.bin.lib import lang

class Npc(BaseModel):
    id = AutoField()
    shortname = CharField(unique=True)
    opinion_of_master_of_whispers = IntegerField(default=0)
    opinion_of_master_of_ceremony = IntegerField(default=0)
    opinion_of_cardinal = IntegerField(default=10)
    opinion_of_marshal = IntegerField(default=0)
    opinion_of_banker = IntegerField(default=0)
    in_game = BooleanField(default=1)

    def name(self):
        return lang('character.'+self.shortname)

    def get_opinion(self, shortname):
        opinion = getattr(self, 'opinion_of_'+shortname)
        return int(opinion)

    @staticmethod
    def find(name):
        return Npc.get(shortname = name)

    @staticmethod
    def factory():
        Npc.create(shortname='duce')
        Npc.create(shortname='duchess')
        Npc.create(shortname='steward')
        Npc.create(shortname='chiara')
        Npc.create(shortname='sofia')
        Npc.create(shortname='taormina')
        Npc.create(shortname='royal_guard')
        Npc.create(shortname='alchemist')
        Npc.create(shortname='ambassador')
        Npc.create(shortname='scribe')
        Npc.create(shortname='clarissa')

        return True

    @staticmethod
    def migrate():
        db.create_tables([Npc])

    @staticmethod
    def rollback():
        db.drop_tables([Npc])

    @staticmethod
    def recreate():
        db.drop_tables([Npc])
        db.create_tables([Npc])
        Npc.factory()

    @staticmethod
    def get_active():
        q = Npc.select().where(Npc.in_game == 1).execute()
        return list(q)
