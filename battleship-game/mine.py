from coord import Coord


class Mine:
    def __init__(self, pos: Coord, damage_radius: int):
        """
        :param pos:             position on filed
        :param damage_radius:   damage radius of mine
        """
        self._pos = pos
        self._damage_radius = damage_radius

    @property
    def pos(self) -> Coord:
        return self._pos

    @property
    def damage_radius(self) -> int:
        return self._damage_radius

    def __repr__(self) -> str:
        return f"Mine(pos={repr(self.pos)}, damage_radius={self.damage_radius})"


class SmallMine(Mine):
    """
    Mine with 1 damage radius
    """
    def __init__(self, pos: Coord):
        super().__init__(pos, 1)
