import sys
from .mapa import (
    load_map,
    CellTypes,
    color_map,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QWidget,
    QGraphicsScene,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsRectItem,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QWheelEvent,
    QBrush,
)

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

        self.cell_size = 20  # pixels

        self.rows, self.cols, self.grid_data = load_map()

        self.scene = QGraphicsScene()
        self.view = ZoomableGridView(self.scene)
        self.view.setMinimumSize(600, 400)

        # Boton editar mapa
        self.editar_mapa = QPushButton("Editar mapa")
        #self.btn_editar.clicked.connect(self.editar_mapa)

        # Boton iniciar Beam Search
        self.btn_beam = QPushButton("Iniciar Beam Search")
        #self.btn_beam.clicked.connect(self.iniciar_beam)

        # Boton iniciar Dynamic Weighting
        self.btn_dw = QPushButton("Iniciar Dynamic Weighting")
        #self.btn_dw.clicked.connect(self.iniciar_dw)

        # Panel lateral
        self.panel = QVBoxLayout()
        self.panel.addWidget(self.editar_mapa)
        self.panel.addWidget(self.btn_beam)
        self.panel.addWidget(self.btn_dw)
        self.panel.addStretch()

        self.side_widget = QWidget()
        self.side_widget.setLayout(self.panel)
        self.side_widget.setFixedWidth(200)

        # Grid + Panel
        self.main_area = QHBoxLayout()
        self.main_area.addWidget(self.view)
        self.main_area.addWidget(self.side_widget)

        #self.size_spin = QSpinBox()
        #self.size_spin.setRange(10, 500)
        #self.size_spin.setValue(self.grid_size)
        #self.size_spin.valueChanged.connect(self.set_grid_size)

        layout = QVBoxLayout()
        layout.addLayout(self.main_area)
        self.setLayout(layout)

        self.redraw_grid()

    def set_grid_size(self, size):
        self.grid_size = size

    def redraw_grid(self):
        self.scene.clear()
        width = self.cols * self.cell_size
        height = self.rows * self.cell_size
        self.scene.setSceneRect(0, 0, width, height)

        for row in range(self.rows):
            for col in range(self.cols):
                cell_type = self.grid_data.get((row, col), CellTypes.EMPTY)
                color = color_map[cell_type]

                rect = QGraphicsRectItem(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                rect.setBrush(QBrush(color))
                self.scene.addItem(rect)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hormigas vs Venenos")
        self.setCentralWidget(GridWidget())