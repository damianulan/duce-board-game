from app.models.autoload import *

def cheat_hit(params):
    shortname = params[2]
    hit_points = params[3]
    if shortname and hit_points:
        player = Player.find(shortname)
        player.hit(int(hit_points))
        return True
    return False