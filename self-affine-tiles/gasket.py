from tile import SelfAffineTile

A = [
    [2, 0],
    [0, 2]
]

D = [
    (0, 0),
    (1, 0),
    (0, 1),
    (-1, -1)
]

x0 = (1/2, 1/2)

Gasket = SelfAffineTile(A, D, x0, "Gasket")
Gasket(10000, 100, True)
