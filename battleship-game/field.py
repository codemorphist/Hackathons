from coord import Coord
from ship import Ship, Orientation
from ship import LinearShip, Frigate, Brig, Gunboat
from mine import Mine

from typing import List, Dict, Union


DefaultRules = {
    LinearShip: 1,
    Frigate: 2,
    Brig: 3,
    Gunboat: 4
}


class ShipIterator:
    """
    Iterate by Ships from Field
    """
    def __init__(self, field): 
        self.i = 0
        self.field = field

    def __iter__(self):
        return self

    def __next__(self):
        try:
            ship = self.field.objects[self.i]
            self.i += 1
            if isinstance(ship, Ship):
                return ship
            else:
                return next(self)
        except IndexError:
            raise StopIteration


class Field:
    def __init__(self, 
                 objects: list[Union[Ship, Mine]], 
                 size: int = 8,
                 rules: Dict[type, int] = DefaultRules):
        """
        :param objects: objects placed on Field
        :param size: size of field
        :param rules: rules for cout of ships
        """
        self._objects = objects
        self._size = size
        self._rules = rules

    @property
    def objects(self):
        return self._objects

    @property
    def size(self):
        return self._size

    def is_ship(self, coord: Coord) -> bool:
        for ship in ShipIterator(self):   
            pass


if __name__ == "__main__":
    f = Field(
        [
            Frigate(Coord(3,2), Orientation.Up),
            Brig(Coord(5, 6), Orientation.Left)
        ]
    )

    for s in ShipIterator(f):
        print(s)
        input()
