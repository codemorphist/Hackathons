from tile import SelfAffineTile

A = [
    [1, 1],
    [-1, 1]
]

D = [
    (0, 0),
    (0, 1)
]

x0 = (1/2, 1/2)


TwinDragon = SelfAffineTile(A, D, x0, "Twin Dragon")
TwinDragon(int(10e5), 20, colorize=True)
