class Coord:
    """
    Coord class is implementation of coodinates
    """

    def __init__(self, 
                 x: int, 
                 y: int ):
        """
        :param x: x coodinate
        :param y: y coodinate
        """ 
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError(f"Invalid type(s) of coordinated")

        self._x = x 
        self._y = y 

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return hash(f"{self._x}:{self._y}")

    def __add__(self, coord):
        sx, sy = self
        cx, cy = coord
        return Coord(sx + cx, sy + cy)

    def __sub__(self, coord):
        return self + (-1 * coord) 

    def __mul__(self, val: int):
        x, y = self 
        return Coord(x * val, y * val)

    def __div__(self, val: int):
        return self * (1 // val)

    def __rmul__(self, val: int):
        return self * val 

    def __eq__(self, coord):
        return tuple(self) == tuple(coord)

    def __repr__(self) -> str:
        return f"Cord(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        """
        Return coodinates in algebraic notation:
        <letter><integer>
        """
        if self.x < 0 or self.x >= 26:
            return f"{tuple(self)}"
        return f"{chr(ord('a') + self.x)}{self.y + 1}"

