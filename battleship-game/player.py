from field import Field


class Player:
    def __init__(self, name: str, field: Field):
        self._name = name
        self._field = field

    @property
    def name(self):
        return self._name

    @property
    def field(self):
        return self._field

    def __repr__(self) -> str:
        return f"Player(name={self.name})"

