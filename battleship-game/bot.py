from enum import Enum, auto
from player import Player
from ship import Orientation
from coord import Coord
from battle import MoveResult, BattleGame
from utils import random_coord, random_field
from random import shuffle
from exceptions import *


class BotLevel(Enum):
    Matroos = auto()
    Capitan = auto()
    Admiral = auto()


class Bot(Player):
    def __init__(self, size: int = 8, level: BotLevel = BotLevel.Matroos):
        super().__init__('Bot', random_field())
        self._level = level

        self._last_move = None
        self._last_move_result = None
        self._queue = []

    def _random_move(self, game: BattleGame) -> Coord:
        move = random_coord()
        while not game.can_attack(move):
            move = random_coord()
        return move

    def _matroos_level(self, game: BattleGame) -> Coord:
        return self._random_move(game)
        
    def _capitan_level(self, game: BattleGame) -> Coord:
        if self._last_move_result is MoveResult.ShipDamaged:
            self._queue = []
            for orient in Orientation:
                move = self._last_move + orient.value
                if game.can_attack(move):
                    self._queue.append(move)
            shuffle(self._queue)
            move = self._queue.pop()
        elif self._last_move_result is MoveResult.ShipDestroyed:
            self._queue = []
            move = self._random_move(game)
        elif self._queue: 
            move = self._queue.pop()
        else:
            move = self._random_move(game) 

        self._last_move = move
        return move

    def _admiral_level(self, game: BattleGame) -> Coord:
        pass

    def get_move(self, game: BattleGame) -> Coord:
        level = self._level
        if level is BotLevel.Matroos:
            return self._matroos_level(game)
        elif leve is BotLevel.Capitan:
            return self._capitan_level(game)
        elif level is BotLevel.Admiral:
            return self._admiral_level(game)
        else:
            raise InvalidBotLevel(level)
       
    def set_result(self, result: MoveResult):
        self._last_move_result = result

