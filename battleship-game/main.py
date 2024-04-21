from battle import BattleGame, BattleStatus, MoveResult
from coord import Coord
from ship import *
from field import *
from mine import *
from player import Player
from ascii import draw_game
from random import randint
from exceptions import *
import os


def random_move(size: int = 8):
    return Coord(randint(0, size-1), randint(0, size-1))


def get_player_move(game: BattleGame) -> Coord:
    move = Coord(*tuple(map(int, input("Ваш хід капітан: ").split())))
    while not game.can_attack(move):
        move = Coord(*tuple(map(int, input("Ви вже били по цій клітині капітан: ").split())))
    return move

def get_bot_move(game: BattleGame) -> Coord:
    move = random_move()    
    while not game.can_attack(move):
        move = random_move()
    return move

def print_result(res: MoveResult, you: bool):
    you_text = {
        MoveResult.Miss: "Ви промахнулися",
        MoveResult.ShipDamaged: "Ви підбили ворожий корабель",
        MoveResult.ShipDestroyed: "Ви знищили ворожий корабель",
        MoveResult.BlowUpMine: "Ви підірвалися на міні"
    }

    other_text = {
        MoveResult.Miss: "Ваш опонент промахнувся",
        MoveResult.ShipDamaged: "Ваш корабль було підбито",
        MoveResult.ShipDestroyed: "Ваш корабль було знищено",
        MoveResult.BlowUpMine: "Ваш противник підірвався на міні"
    }

    print(you_text[res] if you else other_text[res])


def print_status(status: BattleStatus):
    if status is BattleStatus.Player1Win:
        print("Ви виграли знищивши флот противника!")
    else:
        print("Ваш флот було знищено!")


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
            SmallMine(Coord(4, 4))
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
            SmallMine(Coord(4, 4)),
        ]
    )


os.system("clear")
you = Player(input("Введіть ваше ім'я: "), f1)
bot= Player("Бо Джек Т", f2)

game = BattleGame(you, bot)

os.system("clear")
draw_game(game, you)

status = game.status
while True:
    if game.current_player is you:
        you_move = True
        move = get_player_move(game) 
    else:
        you_move = False
        move = get_bot_move(game)

    res, status = game.attack(move)
    
    os.system("clear")
    draw_game(game, you)

    if status is not BattleStatus.Running:
        print_status(status)
        break

    print_result(res, you_move)
    input("Натисніть (Enter) щоб продовжити...")
