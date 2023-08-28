from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import random
import numpy as np


class MplWidget2(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


class MainWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        designer_file = QFile("qt_2.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget2)
        self.ui = loader.load(designer_file, self)

        designer_file.close()

        #self.ui.pushButton.clicked.connect(self.update_graph)
        self.ui.button1.clicked.connect(self.update_graph)

        self.setWindowTitle("PySide2 & Matplotlib Example GUI")

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.ui.asss.canvas.axes.clear()
        self.ui.asss.canvas.axes.plot(t, cosinus_signal)
        self.ui.asss.canvas.axes.plot(t, sinus_signal)
        self.ui.asss.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.ui.asss.canvas.axes.set_title('Cosinus - Sinus Signals')
        self.ui.asss.canvas.draw()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWidget()
    window.show()
    app.exec_()
