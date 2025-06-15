import os 
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import tkinter as tk
from tkinter import filedialog, messagebox
from renderer.tkinter_renderer import TkinterRenderer
from renderer.svg_renderer import SVGRenderer
from listeners.document_model.document_model_listener import DocumentModelListener
from document.document_model import DocumentModel
from geometry.line import LineSegment
from geometry.oval import Oval
from geometry.point import Point
from geometry.composite_shape import CompositeShape
from state.idle_state import IdleState
from state.add_shape_state import AddShapeState
from state.select_shape_state import SelectShapeState
from state.eraser_state import EraserState


class DrawingCanvas(tk.Canvas, DocumentModelListener):
    def __init__(self, parent_gui, document_model):
        super().__init__(parent_gui, bg='white', highlightthickness=0)

        self.gui = parent_gui
        self.document_model = document_model
        self.document_model.add_document_model_listener(self)

        self.focus_set()  # Set focus to the canvas to capture keyboard events

        self.bind('<ButtonPress-1>', self.mouse_down_handler)
        self.bind('<ButtonRelease-1>', self.mouse_up_handler)
        self.bind('<B1-Motion>', self.mouse_dragged_handler)

    def mouse_down_handler(self, event):
        state = self.gui.get_current_state()
        p = Point(event.x, event.y)
        # Determine if shift or ctrl keys are pressed
        shift = (event.state & 0x0001) != 0
        ctrl = (event.state & 0x0004) != 0
        state.mouse_down(p, shift, ctrl)

    def mouse_up_handler(self, event):
        state = self.gui.get_current_state()
        p = Point(event.x, event.y)
        # Determine if shift or ctrl keys are pressed
        shift = (event.state & 0x0001) != 0
        ctrl = (event.state & 0x0004) != 0
        state.mouse_up(p, shift, ctrl)

    def mouse_dragged_handler(self, event):
        state = self.gui.get_current_state()
        p = Point(event.x, event.y)
        state.mouse_dragged(p)

    def key_pressed_handler(self, event):
        state = self.gui.get_current_state()
        key_code = event.keysym
        state.key_pressed(key_code)
        
    def paint(self):
        self.delete('all')
        renderer = TkinterRenderer(self)
        current_state = self.gui.get_current_state()

        for obj in self.document_model.list():
            obj.render(renderer)
            current_state.after_draw(renderer, obj)

        current_state.after_draw(renderer)

    def document_change(self):
        self.paint()


class Paint(tk.Tk):
    def __init__(self, prototypes):
        super().__init__()
        self.title('GoatPaint')
        self.geometry('800x600')

        self.prototypes = prototypes
        self.document_model = DocumentModel()

        self.current_state = IdleState()

        toolbar = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        selection_action = lambda: self.set_state(SelectShapeState(self.document_model))
        select_button = tk.Button(toolbar, text='Select', command=selection_action)
        select_button.pack(side=tk.LEFT, padx=2, pady=2)

        for proto in self.prototypes:
            action = lambda p=proto: self.set_state(
                AddShapeState(self.document_model, p)
                )
            button = tk.Button(toolbar, text=proto.get_shape_name(), command=action)
            button.pack(side=tk.LEFT, padx=2, pady=2)

        eraser_action = lambda: self.set_state(EraserState(self.document_model))
        eraser_button = tk.Button(toolbar, text='Eraser', command=eraser_action)
        eraser_button.pack(side=tk.LEFT, padx=2, pady=2)

        export_button = tk.Button(toolbar, text='Export', command=self.export_to_svg)
        export_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_button = tk.Button(toolbar, text='Save', command=self.save_drawing)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)

        load_button = tk.Button(toolbar, text='Load', command=self.load_drawing)
        load_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.prototype_map = {proto.get_shape_id(): proto for proto in self.prototypes}
        self.prototype_map['@COMP'] = CompositeShape([])

        self.canvas = DrawingCanvas(self, self.document_model)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bind('<Key>', self.key_pressed_handler)

        print('Welcome to Goat Paint!')
        # --- HARD-CODED OBJECTS FOR TESTING ---
        self.document_model.add_graphical_object(LineSegment(Point(50, 50), Point(200, 200)))
        self.document_model.add_graphical_object(Oval(Point(100, 100), Point(300, 200)))
        self.document_model.add_graphical_object(Oval(Point(400, 100), Point(600, 200)))

    def get_current_state(self):
        return self.current_state
    
    def set_state(self, new_state):
        if self.current_state:
            self.current_state.on_leaving()
            
        self.current_state = new_state
        # self.current_state.on_enter(self)

    def key_pressed_handler(self, event):
        key_code = event.keysym
        print(f'Key pressed: {key_code}')
        if key_code == 'Escape':
            self.set_state(IdleState())
        else:
            self.current_state.key_pressed(key_code)
        
    def export_to_svg(self):
        filename = filedialog.asksaveasfilename(
            defaultextension='.svg',
            filetypes=[('SVG (Scalable Vector Graphics) files', '*.svg'), ('All files', '*.*')],
            title='Save SVG File'
        )

        if filename:
            renderer = SVGRenderer(filename)
            for obj in self.document_model.list():
                obj.render(renderer)

            renderer.close()

    def save_drawing(self):
        filename = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
            title='Save Drawing'
        )

        if filename:
            try:
                with open(filename, 'w') as file:
                    rows = []
                    for obj in self.document_model.list():
                        obj.save(rows)
                    file.write('\n'.join(rows))
                messagebox.showinfo('Success', 'Drawing saved successfully!')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save drawing: {e}')

    def load_drawing(self):
        filename = filedialog.askopenfilename(
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
            title='Load Drawing'
        )
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except IOError as e:
            messagebox.showerror('Error', f'Failed to load drawing: {e}')
            return
        
        self.document_model.clear()
        stack = []

        for line in lines:
            line = line.strip()
            if not line: continue

            parts = line.split(' ', 1)
            shape_id = parts[0]
            data = parts[1] if len(parts) > 1 else ''

            prototype = self.prototype_map.get(shape_id)
            if prototype:
                prototype.load(stack, data)
            else:
                messagebox.showerror('Error', f'Unknown shape ID: {shape_id}')
                return
            
        for obj in stack:
            self.document_model.add_graphical_object(obj)

if __name__ == '__main__':
    paint = Paint([LineSegment(), Oval()])
    paint.mainloop()