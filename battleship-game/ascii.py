from battle import BattleGame
from coord import Coord
from field import Field, Attacked
from player import Player
from ship import Ship
from mine import Mine


CYAN = "\u001b[36m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
MAGENTA = "\u001b[35m"
BLUE = "\u001b[34m"
RESET = "\u001b[0m"


def styled(text: str, style: str) -> str:
    return style + text + RESET


def draw_field(field: Field, smoke: bool = False):
    print(" ", BLUE + " ".join([chr(ord("a")+i) for i in range(field.size)]) + RESET)
    r = 1
    for y in range(field.size):
        print(styled(str(r), BLUE), end=" ")
        for x in range(field.size):
            curr = Coord(x, y)
            obj, i = field.get_object(curr, smoke)
            if isinstance(obj, Mine):
                print(styled("o", MAGENTA), end=" ")
            elif isinstance(obj, Ship):
                print(styled("x", RED) if obj.decks[i] else styled("#", RESET), end=" ")
            elif isinstance(obj, Attacked):
                print(styled(".", GREEN), end=" ") 
            else:
                print(styled("~", CYAN), end=" ")
        print()
        r += 1


def draw_game(game: BattleGame, player: Player):
    p1 = game._player1 
    p2 = game._player2

    if player is p2:
        p1, p2 = p2, p1
    print(f"Player <{p1.name}>")
    draw_field(p1.field)
    print(f"Player <{p2.name}>")
    draw_field(p2.field, smoke=True)
    print()

