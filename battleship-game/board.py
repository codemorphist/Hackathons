from enum import Enum, auto
from coord import Coord
from ship import Ship, LinearShip, Frigate, Brig, Gunboat
from mine import Mine, SmallMine


default_rules = {
    LinearShip: 1,    
    Frigate: 2,
    Brig: 3,
    Gunboat: 4,
    SmallMine: 2
}


class ShootResult(Enum):
    Miss = auto()
    ShipDamaged = auto()
    ShipDestroyed = auto()
    MineBlowUp = auto()


class Attacked:
    pass


class Board:
    def __init__(self, 
                 size: int, 
                 objects: list[Ship, Mine] = [].
                 rules = default_rules):
        self._size = size
        self._board = {}
        self._rules = rules
        self.__init_board__(objects)

    def __init_board__(self, objects: list[Ship, Mine]):
        for obj in objects:
            if isinstance(obj, Ship):
                self.place_ship(obj)
            elif isinstance(obj, Mine):
                self.place_mine(obj)
            else:
                raise Exception()

    def place_ship(self, ship: Ship):
        for deck in ship.decks:
            if self.get_object(deck) is not None:
                raise Exception()
            if self._other_ship_near(ship, deck):
                raise Exception()
            self._board[deck] = ship

    def _other_ship_near(self, ship: Ship, pos: Coord) -> bool:
        start = pos + Coord(1, 1)
        end = pos - Coord(1, 1)

        for coord in self.rectangle(start, end):
            if coord == pos:
                continue
            obj = self.get_object(coord) 
            if not isinstance(obj, ship):
                return True
        return False

    def place_mine(self, mine: Mine):
        if get_object(mine.pos) is None:
            self._board[mine.pos] = mine

    def set_attacked(self, coord: Coord):
        

    def on_board(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.size and 0 <= y < self.size

    def get_object(self, coord) -> Ship | Mine | Attacked:
        return self._board.get(coord, None)

    def rectangle(self, start: Coord, end: Coord):
        x1, y1 = start
        x2, y2 = end

        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)
    
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.on_field(Coord(x, y)):
                    yield Coord(x, y)

