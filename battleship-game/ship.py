from enum import Enum
from coord import Coord
from typing import Tuple


class Orientation(Enum):
    Up = Coord(0, -1)
    Left = Coord(-1, 0)
    Right = Coord(1, 0)
    Down = Coord(0, 1)


class Ship:
    def __init__(self, 
                 pos: Coord,
                 size: int, 
                 orient: Orientation):
        """
        :param pos:     position of ship on field
        :param size:    count of ship decks
        :param orient:  orientation of ship
        """
        self._pos = pos
        self._size = size
        self._orient = orient
        
        # Deck notation
        #   0   : undamaged
        #   1   : damaged
        self._decks = [0] * size

    @property
    def pos(self) -> Coord:
        return self._pos

    @property
    def size(self) -> int:
        return self._size

    @property
    def orient(self) -> Orientation:
        return self._orient

    @property
    def decks(self) -> list[int]:
        return self._decks

    def attack_deck(self, index: int):
        if index >= self.size:
            return
        self._decks[index] = 1

    def get_start_end(self) -> Tuple[Coord, Coord]:
        offset = Coord(1, -1) if self.orient in (Orientation.Down, Orientation.Left) else Coord(-1, 1)
        start = self.pos + offset
        end = self.pos + (self.size - 1) * self.orient.value + offset
        return start, end if self.orient in (Orientation.Up, Orientation.Right) else end, start
    

    def get_start_end(self) -> Tuple[Coord, Coord]:
        if self.orient in (Orientation.Up, Orientation.Right):
            start = self.pos + Coord(-1, 1)
            end = self.pos + (self.size-1) * self.orient.value + Coord(1, -1)
            return start, end
        else:
            start = self.pos + Coord(1, -1)
            end = self.pos + (self.size-1) * self.orient.value + Coord(-1, 1)
            return end, start 

    def is_destroyed(self) -> bool:
        return sum(self.decks) == self.size

    def __repr__(self) -> Orientation:
        return f"{type(self).__name__}(pos={repr(self.pos)}, size={self.size}, orientation={self.orient.name}, decks={self.decks})"


class LinearShip(Ship):
    """
    Linear ship class with 4 decks
    """
    def __init__(self, pos: Coord, orient: Orientation):
        return super().__init__(
            pos=pos,
            size=4,
            orient=orient
        )


class Frigate(Ship):
    """
    Frigate ship class with 3 decks
    """
    def __init__(self, pos: Coord, orient: Orientation):
        return super().__init__(
            pos=pos,
            size=3,
            orient=orient
        )


class Brig(Ship):
    """
    Brig ship class with 2 decks
    """
    def __init__(self, pos: Coord, orient: Orientation):
        return super().__init__(
            pos=pos,
            size=2,
            orient=orient
        )


class Gunboat(Ship):
    """
    Gunboat ship class with 1 deck
    """
    def __init__(self, pos: Coord, orient: Orientation):
        return super().__init__(
            pos=pos,
            size=1,
            orient=orient
        )

