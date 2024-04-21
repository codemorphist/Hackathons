from battle import BattleGame
from coord import Coord
from ship import *
from field import *
from player import Player
from ascii import draw_game


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


draw_game(game, p1)

game.attack(Coord(4, 4))

draw_game(game, p2)
