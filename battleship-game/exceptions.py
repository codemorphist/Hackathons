class OutOfField(Exception):
    def __init__(self, obj):
        message = f"{obj} out of field"
        super().__init__(message)


class PlaceError(Exception):
    def __init__(self, obj1, obj2):
        message = f"Can't place {obj1} on {obj2}"
        super().__init__(message)
        

class ShipTooNear(Exception):
    def __init__(self, ship):
        message = f"Ship {ship} too near to other ship(s)"
        super().__init__(message)


class InvalidGameObject(Exception):
    def __init__(self, obj):
        message = f"Invalid object {obj}"
        super().__init__(message)


class InvalidCount(Exception):
    def __init__(self, obj):
        message = f"invalid count of object {obj.__name__}"
        super().__init__(message)


class AlredyAttacked(Exception):
    def __init__(self, coord):
        message = f"You already attacked coord {str(coord)}"
        super().__init__(message)

