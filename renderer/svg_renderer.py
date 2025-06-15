from .renderer import Renderer
from geometry.point import Point


class SVGRenderer(Renderer):
    def __init__(self, file_path):
        self.file_path = file_path
        self.svg_content = []
        self.svg_content.append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">')

    def close(self):
        self.svg_content.append('</svg>')
        with open(self.file_path, 'w') as f:
            f.write('\n'.join(self.svg_content))

    def draw_line(self, start, end):
        tag = f'  <line x1="{start.x}" y1="{start.y}" x2="{end.x}" y2="{end.y}" style="stroke:blue;stroke-width:2" />'
        self.svg_content.append(tag)

    def fill_polygon(self, points):
        points_str = ' '.join(f'{p.x},{p.y}' for p in points)
        tag = f'  <polygon points="{points_str}" style="fill:blue;stroke:red;stroke-width:1" />'
        self.svg_content.append(tag)