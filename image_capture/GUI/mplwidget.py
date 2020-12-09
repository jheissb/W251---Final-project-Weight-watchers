from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class MplWidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.canvas=FigureCanvas(Figure())
        vertical_layout=QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes=self.canvas.figure.add_subplot(111,position = [0.1,0.4,0.85,0.57])#change to adjust for axis labels
        self.setLayout(vertical_layout)
