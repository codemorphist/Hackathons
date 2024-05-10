#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from BalisticCalculatorGUIui import BaliscticCalculatorGUIUI


class BaliscticCalculatorGUI(BaliscticCalculatorGUIUI):
    def __init__(self, master=None, on_first_object_cb=None):
        super().__init__(master, on_first_object_cb=None)


if __name__ == "__main__":
    app = BaliscticCalculatorGUI()
    app.run()
