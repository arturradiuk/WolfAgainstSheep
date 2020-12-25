import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QLabel)
from PyQt5.QtGui import QPainter, QIcon
from model.point_model import Point


class MainLogicThread(QThread):
    element_signal = pyqtSignal(list)
    add_sheep_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MainLogicThread, self).__init__(parent=parent)

    def run(self):
        self.element_signal.emit([Point(1, 1)])

    def stop(self):
        self.terminate()


class MainWindow(QMainWindow):
    width = 500
    height = 500
    wer = 50  # wolf ellipse radius

    cartesian_zero = [width // 2, height // 2]

    draw_elements = []  # points to be drawn

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self._set_configuration()
        # self.mainLogicThread = MainLogicThread(self)
        # self.mainLogicThread.element_signal.connect(self.update_draw_elements)
        # self.mainLogicThread.start()
        self.UiComponents()
        self.show()

    def UiComponents(self):
        step_btn = QPushButton("step", self)
        step_btn.setGeometry(0, 0, 100, 30)
        step_btn.clicked.connect(self.step_button_click)

        reset_btn = QPushButton("reset", self)
        reset_btn.setGeometry(105, 0, 100, 30)
        reset_btn.clicked.connect(self.reset_button_click)

        self.sheep_number_label = QLabel("sheep: 15", self)
        self.sheep_number_label.setGeometry(210, 0, 100, 30)

    def reset_button_click(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information")
        msg.setText("Last sheep has been eaten")
        x = msg.exec_()

    def step_button_click(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText("This is the main text!")
        x = msg.exec_()

    def _set_configuration(self):
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("WolfAgainstSheep - simulation")

    def closeEvent(self, event):
        super(MainWindow, self).closeEvent(event)
        # self.mainLogicThread.stop()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for e in self.draw_elements:
            # self.convert_to_cartesian(e)
            temp_1 = e.x - self.wer // 2
            temp_2 = e.y - self.wer // 2
            painter.drawEllipse(temp_1, temp_2, self.wer, self.wer)

    def update_draw_elements(self, elements):
        self.draw_elements = elements
        self.update()

    def convert_to_cartesian(self, point):
        point.x = point.x + self.cartesian_zero[0]
        point.y = point.y + self.cartesian_zero[1]

    def mousePressEvent(self, QMouseEvent):
        # self.draw_elements = [Point(x=QMouseEvent.pos().x(), y=QMouseEvent.pos().y())]
        # self.update()
        if QMouseEvent.button() == QtCore.Qt.RightButton:
            self.update_draw_elements([Point(x=QMouseEvent.pos().x(), y=QMouseEvent.pos().y())])

        print(QMouseEvent.pos().x())
        print(QMouseEvent.pos().y())


myApp = QApplication(sys.argv)
myApp.setWindowIcon(QIcon("resources/wolf.png"))
window = MainWindow()
myApp.exec_()
sys.exit()
# print(615)
