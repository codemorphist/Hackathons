from tile import SelfAffineTile

A = [
    [3, 0],
    [0, 3]
]

D = [
    (0, 0),
    (1, 0),
    (2, 0),
    (0, 1),
    (0, 2),
    (2, 2),
    (4, 4),
    (2, 1),
    (1, 2)
]

x0 = (1/2, 1/2)

Shooter = SelfAffineTile(A, D, x0, "Shooter")
Shooter(10000, 10)
