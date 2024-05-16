#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
import numpy as np
from calculator import trajectory


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
        self.setup_plots()
        
    def setup_plots(self):
        self.xy_frame = self.builder.get_object("xy_frame")
        self.xy_canvas = tk.Canvas(self.xy_frame, width=380, height=380,
                                   bg="white")
        self.xy_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.xz_frame = self.builder.get_object("xz_frame")
        self.xz_canvas = tk.Canvas(self.xz_frame, width=380, height=380,
                                   bg="white")
        self.xz_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        self.yz_frame = self.builder.get_object("yz_frame")
        self.yz_canvas = tk.Canvas(self.yz_frame, width=380, height=380,
                                   bg="white")
        self.yz_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.image_frame = self.builder.get_object("image_frame")


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

    def parse_data(self):
        roll = self.roll_angle.get()
        pitch = self.pitch_angle.get()
        yaw = self.yaw_angle.get()

        x = self.x_pos.get()
        y = self.y_pos.get()
        z = self.z_pos.get()

        x_vel = self.x_vel.get()
        y_vel = self.y_vel.get()
        z_vel = self.z_vel.get()

        x_wind = self.x_wind.get()
        y_wind = self.y_wind.get()
        z_wind = self.z_wind.get()

        return ((roll, pitch, yaw), (x, y, z)), \
                (x_vel, y_vel, z_vel), (x_wind, y_wind, z_wind)

    def visualize(self, points):
        self.xy_canvas.delete("all")
        for x, y, z in points:
            self.xy_canvas.create_oval(x-2+380/2, -y-2+380/2, x+2+380/2, -y+2+380/2, 
                                       fill="red", outline="red")
            self.xz_canvas.create_oval(x-2+380/2, -z-2+380/2, x+2+380/2, -z+2+380/2, 
                                       fill="red", outline="red")
            self.yz_canvas.create_oval(y-2+380/2, -z-2+380/2, y+2+380/2, -z+2+380/2, 
                                       fill="red", outline="red")

    def calculate_trajectory(self):
        data = self.parse_data()
        points = trajectory(*data)
        self.visualize(points)

    
if __name__ == "__main__":
    app = BaliscticCalculatorGUIUI()
    app.run()
