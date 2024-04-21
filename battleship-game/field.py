from typing import List, Dict, Union, TypeAlias
from coord import Coord
from ship import Ship, Orientation, LinearShip, Frigate, Brig, Gunboat
from mine import Mine, SmallMine
from exceptions import *
from copy import copy


GameObject: TypeAlias = Union[Ship, Mine]
GameObjects: TypeAlias = List[GameObject]


DefaultRules = {
    LinearShip: 1,
    Frigate: 2,
    Brig: 3,
    Gunboat: 4,
    SmallMine: 2
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
        self.can_place_mine(obj)
        self._map[obj.pos] = (obj, None)
        self._update_rule(obj)

    def _place_ship(self, obj: Ship):
        self.can_place_ship(obj)
        curr = obj.pos
        for deck in range(obj.size):
            self._map[curr] = (obj, deck)
            curr += obj.orient.value
        self._ships.append(obj)
        self._update_rule(obj)

    def can_place_mine(self, obj: GameObject):
        if not self.on_field(obj.pos):
            raise OutOfField(obj)
        if obj.pos in self._map:
            raise PlaceError(obj, self.get_object(obj.pos))

    def can_place_ship(self, obj: Ship):
        curr = obj.pos
        for deck in range(obj.size):
            if not self.on_field(curr):
                raise OutOfField(obj)
            if curr in self._map:
                raise PlaceError(obj, self.get_object(curr))
            if self._ship_near(obj, curr):
                raise ShipTooNear(obj)
            curr += obj.orient.value

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
        if not self.on_field(coord):
            raise OutOfField(coord)

        obj, i = self._map.get(coord, (None, None))

        if smoke:
            if isinstance(obj, Ship) and obj.decks[i]:
                return obj, i
            elif isinstance(obj, Attacked):
                return obj, i
            else:
                return None, None

        return obj, i

    def on_field(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.size and 0 <= y < self.size

    def attack(self, 
               coord: Coord, 
               attacked_check: bool = True) -> Union[Ship, Mine, None]:
        obj, i = self.get_object(coord)

        if obj is None or isinstance(obj, Mine):
            self._map[coord] = (Attacked(), None)
        elif isinstance(obj, Ship):
            if attacked_check and obj.decks[i]:
                raise AlreadyAttacked(coord)

            obj.attack_deck(i)
            if obj.is_destroyed():
                start, end = obj.get_start_end()

                for coord in self.iterate_rectangle(start, end):
                    o, _ = self.get_object(coord)
                    if isinstance(o, Ship):
                        continue
                    self._map[coord] = (Attacked(), None)
        elif attacked_check and isinstance(obj, Attacked):
            raise AlreadyAttacked(coord)

        return obj

    def blow_up_mine(self, mine: Mine) -> GameObjects:
        attacked_objects = []
        start = mine.pos + mine.damage_radius * Coord(-1, -1)
        end = mine.pos + mine.damage_radius * Coord(1, 1)

        for coord in self.iterate_rectangle(start, end):
            attacked_objects.append(self.attack(coord, False))
            
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

