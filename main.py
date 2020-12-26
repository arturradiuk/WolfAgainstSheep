import copy
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter, QIcon, QBrush, QPen
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox, QLabel)

import playground
from model.point_model import Point


class MainLogicThread(QThread):
    width = 500
    height = 500
    wer = 50  # wolf ellipse radius

    cartesian_zero = [width // 2, height // 2]  # todo change to Point

    element_signal = pyqtSignal(list)
    add_sheep_signal = pyqtSignal(int)
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    coef = 50

    def __init__(self, parent=None):
        super(MainLogicThread, self).__init__(parent=parent)
        self.simulation = playground.Simulation(sheep_move_dist=self.sheep_move_dist,
                                                wolf_move_dist=self.wolf_move_dist)

    def add_sheep(self, position: Point):
        position = copy.copy(position)
        self.simulation.create_sheep(copy.copy(self.convert_from_cartesian(position)))
        res = []
        temp_pos = self.simulation.get_alive_sheep_positions()
        for i in range(len(temp_pos)):
            res.append(self.convert_to_cartesian(copy.copy(temp_pos[i])))
        return res

    def get_sheep_positions(self):
        res = []
        temp_pos = self.simulation.get_alive_sheep_positions()
        for i in range(len(temp_pos)):
            res.append(self.convert_to_cartesian(copy.copy(temp_pos[i])))
        return res

    def get_wolf_position(self):
        return self.convert_to_cartesian(copy.copy( self.simulation.playground.wolf.position))

    def change_wolf_position(self, position: Point):
        self.simulation.change_wolf_position((self.convert_from_cartesian(position)))
        return self.convert_to_cartesian(copy.copy(self.simulation.playground.wolf.position))

    def run(self):
        self.element_signal.emit([Point(1, 1)])

    def stop(self):
        self.terminate()

    def convert_to_cartesian(self, point):
        point.x = int((point.x + 5) * self.coef)
        point.y = int((point.y + 5) * self.coef)
        return point  # todo check necessity

    def convert_from_cartesian(self, point):
        point.x = (point.x / self.coef) - 5  # can't be casted to int
        point.y = (point.y / self.coef) - 5  # can't be casted to int
        return point

    def run_round(self):
        self.simulation.run_round(self.simulation.round_counter)
        g = 5

class MainWindow(QMainWindow):
    width = 500
    height = 500
    wer = 50  # wolf ellipse radius

    cartesian_zero = [width // 2, height // 2]  # todo change to Point

    draw_elements = []  # points to be drawn

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        self.mainLogicThread = MainLogicThread(self)
        self.mainLogicThread.element_signal.connect(self.update_draw_elements)
        self.wolf_position = self.mainLogicThread.change_wolf_position(
            Point(self.cartesian_zero[0], self.cartesian_zero[1]))

        self._set_configuration()

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
        self.mainLogicThread.run_round()
        self.draw_elements = self.mainLogicThread.get_sheep_positions()
        self.wolf_position = self.mainLogicThread.get_wolf_position()
        self.update()
        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Warning)
        # msg.setWindowTitle("Warning")
        # msg.setText("This is the main text!")
        # x = msg.exec_()

    def _set_configuration(self):
        self.setAutoFillBackground(True)
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("WolfAgainstSheep - simulation")

    def closeEvent(self, event):
        super(MainWindow, self).closeEvent(event)
        # self.mainLogicThread.stop()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for e in self.draw_elements:
            temp_1 = e.x - self.wer // 2
            temp_2 = e.y - self.wer // 2
            painter.setPen(QPen(Qt.black, 12, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            painter.drawEllipse(int(temp_1), int(temp_2), self.wer, self.wer)

        temp_1 = self.wolf_position.x - self.wer // 2
        temp_2 = self.wolf_position.y - self.wer // 2
        painter.setPen(QPen(Qt.black, 12, Qt.SolidLine));
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern));
        painter.drawEllipse(int(temp_1), int(temp_2), self.wer, self.wer)

    def update_draw_elements(self, elements):
        self.draw_elements = elements
        self.update()

    def update_wolf_position(self, position):
        self.wolf_position = self.mainLogicThread.change_wolf_position(position)
        self.update()

    # def convert_to_cartesian(self, point):
    #     point.x = point.x + self.cartesian_zero[0]
    #     point.y = point.y + self.cartesian_zero[1]
    #
    # def convert_from_cartesian(self, point):
    #     point.x = point.x + self.cartesian_zero[0]
    #     point.y = point.y + self.cartesian_zero[1]

    def mousePressEvent(self, QMouseEvent):
        # self.draw_elements = [Point(x=QMouseEvent.pos().x(), y=QMouseEvent.pos().y())]
        # self.update()
        if QMouseEvent.button() == QtCore.Qt.RightButton:
            self.update_wolf_position(Point(QMouseEvent.pos().x(), QMouseEvent.pos().y()))

        # print(QMouseEvent.pos().x())
        # print(QMouseEvent.pos().y())

        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.update_draw_elements(
                self.mainLogicThread.add_sheep(Point(x=QMouseEvent.pos().x(), y=QMouseEvent.pos().y())))


myApp = QApplication(sys.argv)
myApp.setWindowIcon(QIcon("resources/wolf.png"))
window = MainWindow()
myApp.exec_()
sys.exit()
