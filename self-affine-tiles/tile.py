import matplotlib.pyplot as plt 
import numpy as np
from random import choice

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
        self._D = [np.array(v) for v in D]
        self._x0 = np.array(x0)
        self._points = np.array([])

    def __call__(self, N: int, k: int):
        """
        Generate and display the tile.

        Parameters:
            N (int): Number of points to generate.
            k (int): Iteration depth.
        """
        self.generate(N, k)
        self.show()

    def generate(self, N: int, k: int) -> None:
        """
        Generate points for the tile.

        Parameters:
            N (int): Number of points to generate.
            k (int): Iteration depth.
        """
        self._points = np.zeros((N, 2))

        A = self._A
        D = self._D

        for i in range(N):
            x = self._x0
            for j in range(k):
                x = np.dot(A, x)+ choice(D)
            self._points[i] = x

    def show(self) -> None:
        """
        Display the tile.
        """
        if len(self._points) == 0:
            raise Exception("Points is empty. Use generate() before showing it.")

        x_coords = self._points[:, 0]
        y_coords = self._points[:, 1]

        plt.scatter(x_coords, 
                    y_coords,
                    s=10)

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(self._name)
        plt.grid(True)

        plt.show()

