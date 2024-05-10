#!/usr/bin/python3
import pathlib
import tkinter as tk
from matplotlib.figure import Figure
import pygubu

import numpy as np
import matplotlib as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "balistic_app.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class BaliscticCalculatorGUIUI:
    def __init__(self, master=None, on_first_object_cb=None):
        self.builder = pygubu.Builder(
            on_first_object=on_first_object_cb)
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = self.builder.get_object(
            "BalisticSimulator", master)

        self.roll_angle: tk.DoubleVar = None
        self.pitch_angle: tk.DoubleVar = None
        self.yaw_angle: tk.DoubleVar = None
        self.x_pos: tk.DoubleVar = None
        self.y_pos: tk.DoubleVar = None
        self.z_pos: tk.DoubleVar = None
        self.x_vel: tk.DoubleVar = None
        self.y_vel: tk.DoubleVar = None
        self.z_vel: tk.DoubleVar = None
        self.x_wind: tk.DoubleVar = None
        self.y_wind: tk.DoubleVar = None
        self.z_wind: tk.DoubleVar = None
        self.builder.import_variables(self)

        self.builder.connect_callbacks(self)

        self.xy_frame = self.builder.get_object("xy_frame")
        self.xy_figure = Figure(figsize=(4, 4), dpi=100)
        self.xy_canvas = FigureCanvasTkAgg(self.xy_figure, master=self.xy_frame)
        self.xy_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.xy_canvas.draw()

        self.xz_frame = self.builder.get_object("xz_frame")
        self.xz_figure = Figure(figsize=(4, 4), dpi=100)
        self.xz_canvas = FigureCanvasTkAgg(self.xz_figure, master=self.xz_frame)
        self.xz_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.xz_canvas.draw()

        self.yz_frame = self.builder.get_object("yz_frame")
        self.yz_figure = Figure(figsize=(4, 4), dpi=100)
        self.yz_canvas = FigureCanvasTkAgg(self.yz_figure, master=self.yz_frame)
        self.yz_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.yz_canvas.draw()

    def center(self, event):
        wm_min = self.mainwindow.wm_minsize()
        wm_max = self.mainwindow.wm_maxsize()
        screen_w = self.mainwindow.winfo_screenwidth()
        screen_h = self.mainwindow.winfo_screenheight()
        """ `winfo_width` / `winfo_height` at this point return `geometry` size if set. """
        x_min = min(screen_w, wm_max[0],
                    max(self.main_w, wm_min[0],
                        self.mainwindow.winfo_width(),
                        self.mainwindow.winfo_reqwidth()))
        y_min = min(screen_h, wm_max[1],
                    max(self.main_h, wm_min[1],
                        self.mainwindow.winfo_height(),
                        self.mainwindow.winfo_reqheight()))
        x = screen_w - x_min
        y = screen_h - y_min
        self.mainwindow.geometry(f"{x_min}x{y_min}+{x // 2}+{y // 2}")
        self.mainwindow.unbind("<Map>", self.center_map)

    def run(self, center=False):
        if center:
            """ If `width` and `height` are set for the main widget,
            this is the only time TK returns them. """
            self.main_w = self.mainwindow.winfo_reqwidth()
            self.main_h = self.mainwindow.winfo_reqheight()
            self.center_map = self.mainwindow.bind("<Map>", self.center)
        self.mainwindow.mainloop()

    def calculate_trajectory(self):
        self.xy_figure.clear()
        t = np.arange(0, 3, .01)
        self.xy_figure.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        self.xy_canvas.draw()


if __name__ == "__main__":
    app = BaliscticCalculatorGUIUI()
    app.run()
