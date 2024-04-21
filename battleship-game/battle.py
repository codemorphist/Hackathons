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
    ShipDestroyed = auto()
    BlowUpMine = auto()


class BattleGame:
    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2
        self._current_player = self._player1
        self._other_player = self._player2
        self._status = BattleStatus.Running

    @property
    def current_player(self):
        return self._current_player

    @property
    def other_player(self):
        return self._other_player

    def can_attack(self, coord: Coord) -> bool:
        """
        Retrun True if square by coord on field or not attacked
        else raise Exception
        """
        obj, _ = self.other_player.field.get_object(coord, True)
        if isinstance(obj, Attacked):
            return False
        if isinstance(obj, Ship):
            return False
        return True

    def attack(self, coord: Coord) -> Tuple[MoveResult, BattleStatus]: 
        move_result = None
        obj = self.other_player.field.attack(coord)
        if isinstance(obj, Ship):
            if obj.is_destroyed(): 
                move_result = MoveResult.ShipDestroyed
            else:
                move_result = MoveResult.ShipDamaged
            self._update_status()
        elif isinstance(obj, Mine):
            self.current_player.field.blow_up_mine(obj)
            move_result = MoveResult.BlowUpMine
            self._update_status()
            self._switch_turn()
        else:
            move_result = MoveResult.Miss
            self._switch_turn()

        return move_result, self.status

    def _switch_turn(self):
        temp = self._current_player
        self._current_player = self._other_player
        self._other_player = temp

    @property
    def status(self) -> BattleStatus:
        return self._status

    def _update_status(self):
        for ship in self.other_player.field.ships:
            # If player have one undestroyed ship game stay running 
            if not ship.is_destroyed():
                self._status = BattleStatus.Running  
                return

        if self.current_player is self._player1:
            self._status = BattleStatus.Player1Win
        else:
            self._status = BattleStatus.Player2Win

