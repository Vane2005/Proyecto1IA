import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsRectItem, QVBoxLayout, QWidget, QSpinBox, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QBrush, QColor, QWheelEvent

# Cell types
EMPTY = 0
ANT = 1
OBSTACLE = 2
OBJECTIVE = 3

class ZoomableGridView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(self.renderHints())
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event: QWheelEvent):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)

class GridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_size = 50
        self.cell_size = 20  # pixels

        # Sample data: dict of (row, col) -> type
        self.grid_data = {
            (10, 10): ANT,
            (20, 25): OBSTACLE,
            (40, 45): OBJECTIVE,
            (30, 10): OBSTACLE,
        }

        self.scene = QGraphicsScene()
        self.view = ZoomableGridView(self.scene)
        self.view.setMinimumSize(600, 400)

        # Controls
        self.size_spin = QSpinBox()
        self.size_spin.setRange(10, 500)
        self.size_spin.setValue(self.grid_size)
        self.size_spin.valueChanged.connect(self.set_grid_size)

        self.update_btn = QPushButton("Update Grid")
        self.update_btn.clicked.connect(self.redraw_grid)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Grid Size:"))
        controls.addWidget(self.size_spin)
        controls.addWidget(self.update_btn)
        controls.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(controls)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.redraw_grid()

    def set_grid_size(self, value):
        self.grid_size = value

    def redraw_grid(self):
        self.scene.clear()
        self.scene.setSceneRect(0, 0, self.grid_size * self.cell_size, self.grid_size * self.cell_size)

        color_map = {
            EMPTY: QColor(240, 240, 240),
            ANT: QColor(0, 200, 0),        # Green
            OBSTACLE: QColor(200, 0, 0),   # Red
            OBJECTIVE: QColor(0, 100, 200) # Blue
        }

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_type = self.grid_data.get((row, col), EMPTY)
                color = color_map[cell_type]

                rect = QGraphicsRectItem(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                rect.setBrush(QBrush(color))
                self.scene.addItem(rect)

from PySide6.QtWidgets import QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoomable Ant Grid")
        self.setCentralWidget(GridWidget())