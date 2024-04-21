from battle import BattleGame, BattleStatus, MoveResult
from coord import Coord
from ship import *
from field import *
from player import Player
from ascii import draw_game
from random import randint
from exceptions import *


def random_move(size: int = 8):
    return Coord(randint(0, size-1), randint(0, size-1))


f1 = Field(
        [
            LinearShip(Coord(0, 0), Orientation.Down),
            Frigate(Coord(0, 5), Orientation.Down),
            Frigate(Coord(4, 1), Orientation.Left),
            Brig(Coord(6, 0), Orientation.Right),
            Brig(Coord(2, 7), Orientation.Right),
            Brig(Coord(5, 6), Orientation.Up),
            Gunboat(Coord(3, 3), Orientation.Up),
            Gunboat(Coord(2, 5), Orientation.Left),
            Mine(Coord(4, 4), 1)
        ]
    )

f2 = Field(
        [
            LinearShip(Coord(0, 0), Orientation.Down),
            Frigate(Coord(0, 5), Orientation.Down),
            Frigate(Coord(4, 1), Orientation.Left),
            Brig(Coord(6, 0), Orientation.Right),
            Brig(Coord(2, 7), Orientation.Right),
            Brig(Coord(5, 6), Orientation.Up),
            Gunboat(Coord(3, 3), Orientation.Up),
            Gunboat(Coord(2, 5), Orientation.Left),
            Mine(Coord(4, 4), 1)
        ]
    )

p1 = Player("Player1", f1)
p2 = Player("Player2", f2)

game = BattleGame(p1, p2)

# print(game.attack(Coord(0, 0)))
draw_game(game, p1)
# exit()

status = game.status
while status is BattleStatus.Running:
    move = None
    if game._current_player is p1:
        move = Coord(*tuple(map(int, input("Input you move: ").split())))
    else:
        move = random_move()    
        while not game.can_attack(move):
            move = random_move()

    res, status = game.attack(move)
    draw_game(game, p1)
    print(res)
    input()

