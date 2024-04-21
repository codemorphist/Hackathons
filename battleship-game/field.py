from coord import Coord
from ship import Ship, Orientation
from ship import LinearShip, Frigate, Brig, Gunboat
from mine import Mine

from typing import List, Dict, Union
from typing import TypeAlias

from exceptions import *


GameObject: TypeAlias = Union[Ship, Mine]
GameObjects: TypeAlias = List[GameObject]


DefaultRules = {
    LinearShip: 1,
    Frigate: 2,
    Brig: 3,
    Gunboat: 4,
    Mine: 2
}


class Attacked:
    pass


class Field:
    def __init__(self, 
                 objects: GameObject = [], 
                 size: int = 8,
                 rules: Dict[type, int] = DefaultRules):
        """
        :param objects: objects placed on Field
        :param size: size of field
        :param rules: rules for cout of ships
        """
        self._map = {} 
        self._size = size
        self._rules = rules

        self.place_objects(objects)

    def place_objects(self, objects: GameObjects):
        for obj in objects:
            self.place_object(obj)

    def place_object(self, obj: GameObject):
        """
        Place object on field by them coords

        :param obj: object to place
        """
        if isinstance(obj, Mine):
            if not self.on_field(obj.pos):
                raise OutOfField(obj)
            if obj.pos in self._map:
                raise PlaceError(obj, self.get_object(obj.pos))

            self._map[obj.pos] = (obj, None)
            self._change_rule(obj)
        elif isinstance(obj, Ship):
            curr = obj.pos
            for deck in range(obj.size):
                if not self.on_field(curr):
                    raise OutOfField(obj)
                if curr in self._map:
                    raise PlaceError(obj, self.get_object(curr))
                if self._ship_near(obj, curr):
                    raise ShipTooNear(obj)

                self._map[curr] = (obj, deck)
                curr += obj.orient.value
            self._change_rule(obj)
        else:
            raise InvalidGameObject(obj)

    def _ship_near(self, ship: Ship, coord: Coord) -> bool:
        for x in range(coord.x - 1, coord.x + 2):
            for y in range(coord.y - 1, coord.y + 2):
                curr = Coord(x, y)
                if curr == coord:
                    continue
                obj = self.get_object(curr)[0]
                if obj is None:
                    continue
                if isinstance(obj, Ship) and obj is not ship:
                    return True
        return False

    def _change_rule(self, obj: GameObject):
        t = type(obj)
        if t not in self._rules:
            raise InvalidGameObject(obj)
        if self._rules[t] <= 0:
            raise InvalidCount(t)
        else:
            self._rules[t] -= 1

    @property
    def map(self):
        return self._map

    @property
    def size(self):
        return self._size

    def get_object(self, coord: Coord) -> GameObject:
        if coord not in self._map:
            return None, None
        else:
            return self._map[coord]

    def on_field(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.size and 0 <= y < self.size

    def attack(self, coord: Coord) -> Union[Mine, None]:
        obj, info = self.get_object(coord)
        if obj is None:
            self._map[coord] = (Attacked(), None)
        elif isinstance(obj, Ship):
            obj.attack_deck(info)

            if obj.is_destroyed():
                start = obj.pos + Coord(-1, 1)
                end = obj.pos + obj.size * obj.orient.value + Coord(1, 0)

                for c in self._coord_generator(start, end):
                    if not self.on_field(c):
                        continue
                    if c in self._map and self.get_object(c):
                        continue
                    self._map[c] = (Attacked(), None)
        else:
            del self._map[coord]
            return obj
        
    def _coord_generator(self, start: Coord, end: Coord):
        sx, sy = start 
        ex, ey = end
        for y in range(sy, ey-1, -1):
            for x in range(sx, ex+1):
                print(x, y)
                yield Coord(x, y)

if __name__ == "__main__":
    f = Field(
        [
            LinearShip(Coord(0, 0), Orientation.Down),
            Frigate(Coord(0, 5), Orientation.Down),
            Frigate(Coord(2, 0), Orientation.Right),
            Brig(Coord(6, 0), Orientation.Right),
            Brig(Coord(2, 7), Orientation.Right),
            Brig(Coord(5, 6), Orientation.Up),
            Gunboat(Coord(3, 3), Orientation.Up),
            Gunboat(Coord(2, 5), Orientation.Up),
        ]
    )

    f.attack(Coord(5, 6))
    f.attack(Coord(5, 5))

    # f.attack(Coord(2, 5))

    print(" "," ".join([chr(ord("a")+i) for i in range(f.size)]))
    r = 1
    for y in range(f.size):
        print(r, end=" ")
        for x in range(f.size):
            curr = Coord(x, y)
            obj, i = f.get_object(curr)
            if isinstance(obj, Mine):
                print("o", end=" ")
            elif isinstance(obj, Ship):
                print("x" if obj.decks[i] else "#", end=" ")
            elif isinstance(obj, Attacked):
                print(".", end=" ") 
            else:
                print("~", end=" ")
        print()
        r += 1
