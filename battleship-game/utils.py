from coord import Coord
from ship import Ship, Orientation
from mine import Mine
from field import Field, DefaultRules
from exceptions import *
from random import choice, randint, shuffle


def random_coord(size: int = 8) -> Coord:
    return Coord(randint(0, size-1), randint(0, size-1))


def random_oprientation() -> Orientation:
    return choice([o for o in Orientation])


def _random_place_ship(field: Field, ship: type, count: int):
    pass

    
def _random_place_mine(field: Field, mine: type, count: int):
    while True:
        coord = random_coord(field.size)
        m = mine(coord)
        try:
            field.can_place_mine(m)
            field.place_object(m)
        except:
            pass 


def random_field(size: int = 8, rules = DefaultRules) -> Field:
    field = Field(size=size, rules=rules)
    for obj, count in rules.items():
        if issubclass(obj, Ship):
            for _ in range(count):
                _random_place_ship(field, obj, count)
        elif issubclass(obj, Mine):
            for _ in range(count):
                _random_place_mine(field, obj, count)
        else:
            raise InvalidGameObject(obj)

    return field


if __name__ == "__main__":
    from ascii import draw_field
    draw_field(random_field())
