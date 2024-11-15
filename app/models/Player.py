from app.bin.dbengine import *
from app.models.bin.BaseModel import BaseModel
from app.models.Trait import Trait
from app.models.Task import Task
from app.models.Npc import Npc
from app.bin.engine import *
from app.bin.lib import lang, increase_by_percentage


class Player(BaseModel):
    id = AutoField()
    shortname = CharField(unique=True)
    location = CharField(default='corridor')
    influence = IntegerField(default=0) # Punkty Wpływu
    diplomacy = DoubleField(default=0) # Dyplomacja
    intrigue = DoubleField(default=0) # Intryga
    cunning = DoubleField(default=0) # Spryt
    wisdom = DoubleField(default=0) # Mądrość
    xp = DoubleField(default=0) # Doświadczenie
    hp = DoubleField(default=100) # Punkty Życia
    gold = IntegerField(default=0) # Dukaty
    in_game = BooleanField(default=0)

    def name(self):
        return lang('character.'+self.shortname)

    def location_lang(self):
        return lang('location.'+self.location)

    def add_influence(self, influence):
        self.influence = self.influence + int(influence)
        self.save()
        return True

    def remove_influence(self, influence):
        self.influence = self.influence - int(influence)
        if self.influence < 0:
            self.influence = 0

        if self.influence == 0:
            self.in_game = 0
            print("Gracz "+self.name()+" został wyeliminowany z rozgrywki - wartość PW spadła do zera!")
        self.save()
        return True

    def add_intrigue(self, intrigue):
        self.intrigue = self.intrigue + float(intrigue)
        self.save()
        return True

    def remove_intrigue(self, intrigue):
        self.intrigue = self.intrigue - float(intrigue)
        if self.intrigue < 0:
            self.intrigue = 0
        self.save()
        return True

    def add_diplomacy(self, diplomacy):
        self.diplomacy = self.diplomacy + float(diplomacy)
        self.save()
        return True

    def remove_diplomacy(self, diplomacy):
        self.diplomacy = self.diplomacy - float(diplomacy)
        if self.diplomacy < 0:
            self.diplomacy = 0
        self.save()
        return True

    def add_wisdom(self, wisdom):
        self.wisdom = self.wisdom + float(wisdom)
        self.save()
        return True

    def remove_wisdom(self, wisdom):
        self.wisdom = self.wisdom - float(wisdom)
        if self.wisdom < 0:
            self.wisdom = 0
        self.save()
        return True

    def add_cunning(self, cunning):
        self.cunning = self.cunning + float(cunning)
        self.save()
        return True

    def remove_cunning(self, cunning):
        self.cunning = self.cunning - float(cunning)
        if self.cunning < 0:
            self.cunning = 0
        self.save()
        return True

    def add_gold(self, gold):
        self.gold = self.gold + int(gold)
        self.save()
        return True

    def remove_gold(self, gold):
        self.gold = self.gold - int(gold)
        result = True
        if self.gold < 0:
            self.gold = 0
            result = False
        else :
            self.save()
        return result

    def add_xp(self, xp_added):
        self.xp = self.xp + float(xp_added)
        self.save()

    def hit(self, hit_points):
        self.hp = self.hp - float(hit_points)
        if self.hp < 0:
            self.hp = 0
            self.in_game = 0
            print("Gracz "+self.name()+" został wyeliminowany z rozgrywki - wartość HP spadła do zera!")
        self.save()

    def recover(self, recovery_points):
        self.hp = self.hp + float(recovery_points)
        if self.hp > 100 :
            self.hp = 100
        if self.hp > 0 and self.in_game == 0 and self.influence > 0 :
            self.in_game = 1
            print("Gracz "+self.name()+" został przywrócony do życia - wartość HP została odnowiona!")
        self.save()

    def is_available(self):
        if self.location in LOCATIONS and self.in_game == 1:
            return True
        return False

    def can_take_actions(self):
        result = True
        if self.location == DUNGEON:
            print(self.name() + " przybywa aktualnie w Lochu, nie może podejmować żadnych działań.")
            result = False
        if self.location == CORRIDOR:
            print(self.name() + " przebywa aktualnie w korytarzu, aby podjąć działanie należy zmienić lokację.")
            result = False
        if self.hp <= 10:
            print(self.name() + " jest obecnie zbyt osłabiony/a, aby podjąć jakąkolwiek akcję... [HP: "+str(self.hp)+"]")
            result = False
        return result

    def print_stats(self):
        name = self.name()
        influence = str(self.influence)
        intrigue = str(self.intrigue)
        wisdom = str(self.wisdom)
        cunning = str(self.cunning)
        gold = str(self.gold)
        xp = str(self.xp)
        hp = str(self.hp)

        print("### " + name + "\n"
              "Lokalizacja: " + self.location_lang() + "\n"
              "Punkty Wpływu: "+ influence + "\n"
              "Punkty Intryg: "+ intrigue + "\n"
              "Spryt: " + cunning + "\n"
              "Wiedza: " + wisdom + "\n\n"
              "Dukaty: " + gold + "\n"
              "Punkty Życia: " + hp + "\n"
              "Doświadczenie: " + xp + "\n\n"
              )

    def add_trait(self, traitcode, echo = False):
        Trait.create(player=self.id, traitcode=traitcode)
        if echo :
            print("Gracz " +self.name() + " uzyskał nową cechę: " + lang('trait.'+traitcode))

        return True

    def traits(self):
        q = Trait.select().where(Trait.player==self.id).execute()
        return list(q)

    def has_trait(self, traitcode):
        q = list(Trait.select().where(Trait.player==self.id, traitcode=traitcode).execute())
        if q :
            return True
        return False

    def add_task(self, codename):
        if not self.get_task(codename):
            Task.create(player=self.id, codename=codename)
        return True

    def tasks(self):
        q = Task.select().where(Task.player==self.id, Task.finished==0).execute()
        return list(q)

    def get_task(self, codename):
        q = list(Task.select().where(Task.player==self.id, Task.codename == codename, Task.finished==0).execute())
        return q if len(q)>0 else False

    def modify_relations(self, npcname, modifier):
        npc = Npc.find(npcname)
        if npc :
            key = 'opinion_of_' + self.shortname
            relations = getattr(npc, key)
            setattr(npc, key, (relations + modifier))
            npc.save()

    def get_relation(self, npcname):
        npc = Npc.find(npcname)
        if npc :
            key = 'opinion_of_' + self.shortname
            return getattr(npc, key)

        return False

    def process_turn(self):
        base_recovery = 5
        if self.has_trait(Trait.RESILIENT) :
            base_recovery = increase_by_percentage(base_recovery,20)

        self.recover(base_recovery)
        return True

    @staticmethod
    def find(name):
        return Player.get(shortname = name)

    @staticmethod
    def factory():
        Player.create(shortname='master_of_whispers', influence=10, diplomacy=0, intrigue=5, wisdom=0, cunning=0, gold=10)
        Player.create(shortname='master_of_ceremony', influence=10, diplomacy=0, intrigue=0, wisdom=0, cunning=5, gold=10)
        Player.create(shortname='cardinal', influence=25, diplomacy=0, intrigue=0, wisdom=2, cunning=0, gold=10)
        Player.create(shortname='marshal', influence=10, diplomacy=0, intrigue=0, wisdom=2, cunning=2, gold=10)
        Player.create(shortname='banker', influence=10, diplomacy=3, intrigue=0, wisdom=0, cunning=0, gold=20)

        return True

    @staticmethod
    def migrate():
        db.create_tables([Player])

    @staticmethod
    def rollback():
        db.drop_tables([Player])

    @staticmethod
    def recreate():
        db.drop_tables([Player])
        db.create_tables([Player])
        Player.factory()

    @staticmethod
    def get_active():
        q = Player.select().where(Player.in_game==1).execute()
        return list(q)


    # MODIFIERS
    def scheme_modifier(self, weight = 1):
        base_modifier = 0
        if self.has_trait(Trait.PUPPETEER) :
            base_modifier += 5
        if self.has_trait(Trait.SPY) :
            base_modifier += 10

        return base_modifier * weight

    def defence_modifier(self, weight = 1):
        base_modifier = 0
        base_modifier = int(base_modifier + self.cunning)
        if self.has_trait(Trait.FOX) :
            base_modifier += 8
        return base_modifier

    def get_xp_modifier(self):
        modifier = 0
        if self.xp > 5 :
            modifier = 1
        if self.xp > 10 :
            modifier = 2
        if self.xp > 30 :
            modifier = 3
        if self.xp > 50 :
            modifier = 4
        if self.xp > 75 :
            modifier = 5
        return modifier

    def get_xp_modifier_sm(self):
        modifier = self.get_xp_modifier()
        if modifier > 0 :
            modifier = modifier / 2
        return int(modifier)