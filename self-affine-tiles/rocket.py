from tile import SelfAffineTile

A = [
    [3, 0],
    [0, 3]
]

D = [
    (0, 0),
    (1, 1),
    (2, 2),
    (-1, 0),
    (-2, 0),
    (-1, 1),
    (0, -1),
    (0, -2),
    (1, -1)
]

x0 = (1/2, 1/2)

Rocket = SelfAffineTile(A, D, x0, "Rocket")
Rocket(100000, 20, True)
