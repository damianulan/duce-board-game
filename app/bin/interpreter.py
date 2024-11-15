from app.bin.engine import *
from app.models.autoload import *
from app.bin.lib import *
from app.bin.cheatlib import *
from app.classes.SchemeController import SchemeController

def ask(command):
    params = command.split(" ")
    output = False
    if params[0] and params[0].lower().split() != "":
        match params[0]:
            case "start":
                output = gamestart(params)
            case "move":
                output = make_move(params)
            case "action":
                output = make_action(params)
            case "scheme":
                output = make_scheme(params)
            case "end_turn":
                output = next_turn(params)
            case "help":
                output = print_helper(params)
            case "clear_cache":
                output = clear_cache()
            case "stats":
                output = stats_all()
            case "cheat":
                output = cheat_sheet(params)
            case _:
                output = command_default()
    return output

def command_default():
    danger("(!) Error: Nie rozpoznano komendy. Jeśli potrzebujesz pomocy, skorzystaj z polecenia help")
    return False

def clear_cache():
    clean_cache()
    return True

def gamestart(params):
    print("Rozpoczynam nową grę ...")
    reinitialize_models()
    clean_cache()
    result = False
    players_cmd = input("Zainizjowano nową rozgrywkę.\n\nPodaj graczy uczestniczących w nowej rozgrywce.\n"
                        "Do wyboru masz następujące postacie. Pamiętaj aby rozdzielić je średnikiem przy dodawaniu\n"
                        "### master_of_whispers; master_of_ceremony; cardinal; marshal; banker ###\n\n")

    while not result:
        players = []
        players_raw = players_cmd.split(';')
        for p in players_raw:
            player = p.strip()
            if player in PLAYERS_WHITELIST:
                players.append(player)
            else:
                print("Nie rozpoznano postaci: "+ player)
        if len(players) >= 2:
            result = True

            for player in players:
                query = Player.update(in_game=1).where(Player.shortname == player)
                query.execute()

            print("Gra została zinicjalizowana, rozgrywkę rozpoczynają:")
            print(players)
        else:
            players_cmd = input("Wymaganych jest co najmniej dwóch graczy\n")

    if result:
        Game.next_turn()

    return result

def next_move():
    result = False
    while not result:
        command = input("W oczekiwaniu na następny ruch gracza...\n")
        result = ask(command)
    return result

def make_move(params):
    shortname = params[1] if 1 < len(params) else None
    location = params[2] if 2 < len(params) else None

    if shortname and location:
        player = Player.find(shortname)
        if player.is_available():
            result = Move.move_to(shortname, location)
            return result
        else :
            warning('Gracz nie jest aktywny w tej turze!')
    return False

def make_action(params):
    shortname = params[1] if 1 < len(params) else None
    taskcode = params[2] if 2 < len(params) else None

    if shortname:
        res = Move.make_action(shortname, taskcode)
        return res
    return False

def make_scheme(params):
    shortname = params[1] if 1 < len(params) else None
    schemecode = params[2] if 2 < len(params) else None
    operator = params[3] if 3 < len(params) else None

    if shortname and schemecode:
        res = SchemeController.makescheme(shortname, schemecode, operator)
        return res
    else :
        if not shortname :
            danger("Nie wskazano Gracza.")
        if not schemecode :
            danger("Nie podano identyfikatora schematu.")
    return False

def next_turn(params):
    turn = Game.next_turn()
    success("Zainicjowano kolejną turę. ["+str(turn)+"]")

    return True

def print_helper(params):
    print("** This is command helper ** \n"
          "start - Rozpoczyna nową grę reinicjalizując statystyki. Poprzedni stan gry zostanie utracony\n"
          "move [player] [location] - przenosi wskazanego gracza do nowej lokacji na mapie gry. Dostępne lokacje: "+'; '.join(LOCATIONS)+". Dostępni gracze: "+'; '.join(PLAYERS_WHITELIST)+"\n"
          "action [player] - wymusza akcję dla danego gracza w danej turze \n"
          "q - quits the game \n"
          )
    return True

def stats_all():
    players = Player.get_active()
    for player in players:
        player.print_stats()

    return True

def cheat_sheet(params):
    output = False
    if params[1] and params[1] != "":
        match params[1]:
            case "hit":
                output = cheat_hit(params)
            case _:
                output = command_default()
    return output