import tkinter as tk
from renderer.renderer import Renderer
from geometry.point import Point


class TkinterRenderer(Renderer):
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas

    def draw_line(self, start, end):
        self.canvas.create_line(start.x, start.y, end.x, end.y, fill='blue', width=2)

    def fill_polygon(self, points):
        tk_points = [(p.x, p.y) for p in points]

        if tk_points:
            self.canvas.create_polygon(tk_points, fill='blue', outline='red', width=2)