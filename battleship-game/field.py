from typing import List, Dict, Union, TypeAlias
from coord import Coord
from ship import Ship, Orientation, LinearShip, Frigate, Brig, Gunboat
from mine import Mine
from exceptions import *
from copy import copy


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
    def __repr__(self) -> str:
        return "Attacked()"


class Field:
    def __init__(self, 
                 objects: GameObjects = [], 
                 size: int = 8, 
                 rules: Dict[type, int] = DefaultRules):
        self._map = {}
        self._ships = []
        self._size = size
        self._rules = copy(rules)
        self.place_objects(objects)

    def place_objects(self, objects: GameObjects):
        for obj in objects:
            self.place_object(obj)

    def place_object(self, obj: GameObject):
        if isinstance(obj, Mine):
            self._place_mine(obj)
        elif isinstance(obj, Ship):
            self._place_ship(obj)
        else:
            raise InvalidGameObject(obj)

    def _place_mine(self, obj: Mine):
        if not self.on_field(obj.pos):
            raise OutOfField(obj)
        if obj.pos in self._map:
            raise PlaceError(obj, self.get_object(obj.pos))
        self._update_rule(obj)
        self._map[obj.pos] = (obj, None)

    def _place_ship(self, obj: Ship):
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
        self._update_rule(obj)
        self._ships.append(obj)

    def _ship_near(self, ship: Ship, coord: Coord) -> bool:
        start = coord + Coord(-1, -1)
        end = coord + Coord(1, 1)
        for curr in self.iterate_rectangle(start, end):
            if curr == coord:
                continue
            obj, _ = self.get_object(curr)
            if isinstance(obj, Ship) and obj is not ship:
                    return True
            else:
                continue
        return False

    def _update_rule(self, obj: GameObject):
        t = type(obj)
        if t not in self._rules:
            raise InvalidGameObject(obj)
        elif self._rules[t] < 1:
            print(self._rules)
            raise InvalidCount(t)
        else:
            self._rules[t] -= 1

    @property
    def map(self):
        return self._map

    @property
    def ships(self):
        return self._ships

    @property
    def size(self):
        return self._size

    def get_object(self, coord: Coord, smoke: bool=False) -> GameObject:
        obj, i = self._map.get(coord, (None, None))

        if smoke:
            if isinstance(obj, Ship) and obj.is_destroyed():
                return obj, i
            if isinstance(obj, Attacked):
                return obj, i

        return obj, i

    def on_field(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.size and 0 <= y < self.size

    def attack(self, coord: Coord) -> Union[Ship, Mine, None]:
        obj, i = self.get_object(coord)
        if obj is None or isinstance(obj, Mine):
            self._map[coord] = (Attacked(), None)
        elif isinstance(obj, Ship):
            obj.attack_deck(i)
            if obj.is_destroyed():
                start, end = obj.get_start_end()

                for coord in self.iterate_rectangle(start, end):
                    obj, _ = self.get_object(coord)
                    if isinstance(obj, Ship):
                        continue
                    self._map[coord] = (Attacked(), None)
        return obj

    def blow_up_mine(self, mine: Mine) -> GameObjects:
        attacked_objects = []
        start = mine.pos + mine.damage_radius * Coord(-1, -1)
        end = mine.pos + mine.damage_radius * Coord(1, 1)

        for coord in self.iterate_rectangle(start, end):
            attacked_objects.append(self.attack(coord))
            
        return attacked_objects
   
    def iterate_rectangle(self, start: Coord, end: Coord):
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


if __name__ == "__main__":
    f = Field(
        [
            LinearShip(Coord(0, 0), Orientation.Down),
            Frigate(Coord(0, 5), Orientation.Down),
            Frigate(Coord(4, 1), Orientation.Left),
            Brig(Coord(6, 0), Orientation.Right),
            Brig(Coord(2, 7), Orientation.Right),
            Brig(Coord(5, 6), Orientation.Up),
            Gunboat(Coord(3, 3), Orientation.Up),
            Gunboat(Coord(2, 6), Orientation.Left),
            Mine(Coord(4, 4), 8)
        ]
    )

    CYAN = "\u001b[36m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    MAGENTA = "\u001b[35m"
    BLUE = "\u001b[34m"
    RESET = "\u001b[0m"


    print(" ", BLUE + " ".join([chr(ord("a")+i) for i in range(f.size)]) + RESET)
    r = 1
    for y in range(f.size):
        print(BLUE + str(r) + RESET, end=" ")
        for x in range(f.size):
            curr = Coord(x, y)
            obj, i = f.get_object(curr)
            if isinstance(obj, Mine):
                print(MAGENTA + "o" + RESET, end=" ")
            elif isinstance(obj, Ship):
                print(((RED + "x") if obj.decks[i] else (RESET + "#")) + RESET, end=" ")
            elif isinstance(obj, Attacked):
                print(GREEN + "." + RESET, end=" ") 
            else:
                print(CYAN + "~" + RESET, end=" ")
        print()
        r += 1
