import matplotlib.pyplot as plt 
import numpy as np
from copy import copy
from random import randint


class SelfAffineTile:
    """
    Class for generating and displaying self-affine tiles.
    """
    def __init__(self, A, D, x0, name: str="Self Affine Tile"):
        """
        Initialize SelfAffineTile object.

        Parameters:
            A (array-like): Affine transformation matrix.
            D (array-like): List of displacement vectors.
            x_0 (array-like): Initial point.
            name (str, optional): Name of the tile.
        """
        self._name = name
        self._A = np.array(A)
        self._q = abs(np.linalg.det(self._A)) # |det(A)|
        self._D = [np.array(v) for v in D]
        self._x0 = np.array(x0)
        self._points = np.array([])

        self._colors = []

    def __call__(self, N: int, k: int, colorize: bool=False):
        """
        Generate and display the tile.

        Parameters:
            N (int): Number of points to generate.
            k (int): Iteration depth.
            colorize (bool): Colorize dots
        """
        self.generate(N, k)
        self.show(colorize)

    def generate(self, N: int, k: int) -> None:
        """
        Generate points for the tile.

        Parameters:
            N (int): Number of points to generate.
            k (int): Iteration depth.
        """
        self._points = np.zeros((N, 2))
        self._colors = []

        A = self._A
        D = self._D

        for l in range(N):
            x = copy(self._x0)
            c = 0
            q = self._q
            for j in range(k+1):
                i = randint(0, len(D)-1)
                x = np.dot(A, x) + D[i]

                c = c * q + i
            self._points[l] = x
            self._colors.append(c)

    def show(self, colorize: bool=False) -> None:
        """
        Display the tile.

        Parameters:
            colorize (bool): Colorize dots
        """
        if len(self._points) == 0:
            raise Exception("Points is empty. Use generate() before showing it.")

        x_coords = self._points[:, 0]
        y_coords = self._points[:, 1]

        if not colorize:
            plt.scatter(x_coords, y_coords, s=1)
        else:
            plt.scatter(x_coords, y_coords, s=1,
                        c=self._colors, cmap="plasma")

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(self._name)
        plt.grid(True)

        plt.show()

