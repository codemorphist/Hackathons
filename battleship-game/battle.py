from enum import Enum, auto
from coord import Coord
from field import Field, Attacked
from player import Player
from ship import Ship, Orientation, LinearShip, Frigate, Brig, Gunboat
from mine import Mine
from exceptions import *


class BattleStatus(Enum):
    Running = auto()
    Player1Win = auto()
    Player2Win = auto()


class MoveResult(Enum):
    Miss = auto()
    ShipDamaged = auto()
    BlowUpMine = auto()


class Battle:
    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2
        self._current_player = self._player1
        self._other_player = self._player2
        self._status = BattleStatus.Running

    def attack(self, coord: Coord) -> MoveResult: 
        # Check coord already attacked
        obj, _ = self._other_player.field.get_object(coord)
        if isinstance(obj, Attacked):
            raise AlreadyAttacked(coord)

        move_result = None
        obj = self._other_player.field.attack(coord)
        if obj is None:
            move_result = MoveResult.Miss
        elif isinstance(obj, Ship):
            move_result = MoveResult.ShipDamaged
        elif isinstance(obj, Mine):
            self._current_player.field.blow_up_mine(obj)
            move_result = MoveResult.BlowUpMine

        self._update_status()
        self._current_player, self._other_player = self._other_player, self._current_player
        return move_result

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


if __name__ == "__main__":
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
            Mine(Coord(4, 4), 8)
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
            Mine(Coord(4, 4), 8)
        ]
    )

    p1 = Player("Player1", f1)
    p2 = Player("Player2", f2)

    game = Battle(p1, p2)

    print(game.attack(Coord(4, 4)))
