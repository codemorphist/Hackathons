from enum import Enum, auto
from coord import Coord
from field import Field, Attacked
from player import Player
from ship import Ship, Orientation, LinearShip, Frigate, Brig, Gunboat
from mine import Mine
from exceptions import *
from typing import Tuple


class BattleStatus(Enum):
    Running = auto()
    Player1Win = auto()
    Player2Win = auto()


class MoveResult(Enum):
    Miss = auto()
    ShipDamaged = auto()
    BlowUpMine = auto()


class BattleGame:
    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2
        self._current_player = self._player1
        self._other_player = self._player2
        self._status = BattleStatus.Running

    def attack(self, coord: Coord) -> Tuple[MoveResult, BattleStatus]: 
        # Check coord already attacked
        obj, _ = self._other_player.field.get_object(coord)
        if isinstance(obj, Attacked):
            raise AlreadyAttacked(coord)

        move_result = None
        obj = self._other_player.field.attack(coord)
        if isinstance(obj, Ship):
            move_result = MoveResult.ShipDamaged
        elif isinstance(obj, Mine):
            destroyed = self._current_player.field.blow_up_mine(obj)
            move_result = MoveResult.BlowUpMine
        else:
            move_result = MoveResult.Miss

        self._update_status()
        self._switch_turn()
        return move_result, self.status

    def _switch_turn(self):
        self._current_player, self._other_player = self._other_player, self._current_player

    @property
    def status(self) -> BattleStatus:
        return self._status

    def _update_status(self):
        for ship in self._other_player.field.ships:
            # If player have one undestroyed ship game continue
            if not ship.is_destroyed():
                self._status = BattleStatus.Running  
                return
        if self._current_player is self._player1:
            self._status = BattleStatus.Player1Win
        else:
            self._status = BattleStatus.Player2Win

