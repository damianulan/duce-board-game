from app.models.Player import Player
from app.models.Npc import Npc
from app.models.Trait import Trait
from app.models.Task import Task
from app.models.gear.Game import Game
from app.models.gear.Move import Move
from app.models.gear.UsedDeck import UsedDeck

def reinitialize_models():
    Player.recreate()
    Game.recreate()
    Move.recreate()
    Npc.recreate()
    Trait.recreate()
    Task.recreate()
    UsedDeck.recreate()

    return True