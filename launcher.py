from app.bin.dbengine import *
from app.bin.autoload import *

highlight('Witaj w grze planszowej Książę. Będę twoim game masterem.\nAby rozpocząć, lub wznowić rozgrywkę, skorzystaj z poleceń konsolowych. Ich pełną listę znajdziesz pod skryptem "help" ')
command = input()
while command != "q":
    ask(command)
    command = input("\n* W oczekiwaniu na ruch gracza... *\n")