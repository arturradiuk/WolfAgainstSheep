import sys
import time

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QIcon
from model.point_model import Point


class MainLogicThread(QThread):
    element_signal = pyqtSignal(list)
    add_sheep_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MainLogicThread, self).__init__(parent=parent)

    def run(self):
        time.sleep(2)
        self.element_signal.emit([Point(0, 0)])

    def stop(self):
        self.terminate()


class MainWindow(QWidget):
    width = 500
    height = 500
    wer = 50  # wolf ellipse radius

    cartesian_zero = [width // 2, height // 2]

    draw_elements = []  # points to be drawn

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self._set_configuration()
        self.mainLogicThread = MainLogicThread(self)
        self.mainLogicThread.element_signal.connect(self.update_draw_elements)
        self.mainLogicThread.start()

        # self.draw_elements.append(Point(0, 0))
        self.show()

    def _set_configuration(self):
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("WolfAgainstSheep - simulation")

    def closeEvent(self, event):
        super(MainWindow, self).closeEvent(event)
        self.mainLogicThread.stop()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for e in self.draw_elements:
            self.convert_to_cartesian(e)
            painter.drawEllipse(e.x - self.wer // 2, e.y - self.wer // 2, self.wer, self.wer)

    def update_draw_elements(self, elements):
        self.draw_elements = elements
        self.update()

    def convert_to_cartesian(self, point):
        point.x = point.x + self.cartesian_zero[0]
        point.y = point.y + self.cartesian_zero[1]


myApp = QApplication(sys.argv)
myApp.setWindowIcon(QIcon("resources/wolf.png"))
window = MainWindow()
myApp.exec_()
sys.exit()
