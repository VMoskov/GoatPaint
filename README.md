# GoatPaint - Vector Editor for real Goats 🐐🎨

Welcome to **GoatPaint**, a simple vector graphics editor built using Python's standard Tkinter library. This project was developed as a comprehensive exercise to explore and implement several core software design patterns in a practical application. It serves as the graphical companion to the "GoatPad" text editor.

---

## Features

- **Vector Shape Drawing**: Add basic shapes like Lines and Ovals to the canvas.
- **Advanced Object Selection**: A dedicated selection tool to click and select one or more objects (using `Ctrl`).
- **Object Manipulation**:
  - Move selected objects using the arrow keys.
  - Resize and reshape a single selected object by dragging its "hot-points".
- **Z-Ordering**: Change the stacking order of objects using the `+` and `-` keys to bring them forward or send them backward.
- **Composite Objects**:
  - **Group** multiple selected objects into a single object with the `G` key.
  - **Ungroup** a composite object back into its individual components with the `U` key.
- **Eraser Tool**: A free-form eraser that deletes any object its path intersects upon mouse release.
- **File Operations**:
  - **SVG Export**: Save drawings in the standard Scalable Vector Graphics (.svg) format.
  - **Native Save/Load**: Save your work in a custom, human-readable text format and load it back into the editor.

## Design Patterns Implemented

A key goal of this project was the practical application of software design patterns. The following patterns are central to its architecture:

-   **State Pattern**: The core of the application's interactivity. The behavior of mouse clicks, drags, and key presses changes dramatically depending on the currently selected tool (e.g., `AddShapeState`, `SelectShapeState`, `EraserState`). This keeps the main GUI code clean and delegates all tool-specific logic to the corresponding state object.

-   **Bridge Pattern**: Decouples the abstract concept of "rendering" a shape from the concrete implementation of how it's rendered. The `Renderer` interface defines *what* can be drawn (`drawLine`, `fillPolygon`), while concrete implementations like `TkinterRendererImpl` (draws to the screen) and `SVGRendererImpl` (writes to an SVG file) provide the *how*.

-   **Composite Pattern**: Allows a group of objects to be treated in the same way as a single object. The `CompositeShape` class implements the same `GraphicalObject` interface as simple shapes, allowing the model to handle rendering, translating, and selecting a group without needing to know its internal composition.

-   **Observer Pattern**: Creates a robust, decoupled notification system. The `DocumentModel` "observes" every `GraphicalObject` for changes. In turn, the `DrawingCanvas` observes the `DocumentModel`. This creates a chain of updates that ensures the UI is always in sync with the data without tightly coupling components.

-   **Prototype Pattern**: Used to create new shapes. The toolbar holds a "prototype" instance of each available shape. When the "Add Shape" tool is active, it simply calls `duplicate()` on the current prototype to create a new, independent object to be placed on the canvas.

## Project Structure

The project is organized into packages to maintain a clean separation of concerns:

```
/
├── paint.py                 # Main entry point of the application
│
├── document/
│   └── document_model.py    # Manages the collection of all shapes
│
├── geometry/
│   ├── graphical_object.py  # Abstract interface for all shapes
│   ├── line.py, oval.py     # Concrete simple shapes
│   ├── composite_shape.py   # The composite shape for grouping
│   ├── point.py, rectangle.py # Basic geometry classes
│   └── utils.py             # Geometry helper functions
│
├── gui/
│   └── tkinter_renderer.py  # Renderer for drawing on the Tkinter canvas
│
├── listeners/
│   └── ...                  # Interfaces for the Observer pattern
│
├── renderer/
│   ├── renderer.py          # The abstract Renderer interface (Bridge pattern)
│   └── svg_renderer.py      # Renderer for exporting to SVG files
│
└── states/
└── ...                  # All concrete states (Idle, Select, Add, Erase, etc.)
```

## How to Run

No external libraries are required, as the project uses Python's built-in `tkinter` library.

1.  Clone the repository.
2.  Navigate to the project's root directory.
3.  Run the main application file from your terminal:
    ```bash
    python paint.py
    ```
