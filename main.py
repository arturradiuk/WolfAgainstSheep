import copy
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter, QIcon, QBrush, QPen
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox, QLabel, QSlider, QAction,
                             QColorDialog)

import playground
from model.point_model import Point

WindowWidth = 500
WindowHeight = WindowWidth  # suppose that height = width


class MainLogicThread(QThread):
    element_signal = pyqtSignal(list)
    add_sheep_signal = pyqtSignal(int)

    def set_simulation_parameters(self, sheep_move_dist, wolf_move_dist, init_pos_limit, WindowWidth):
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.init_pos_limit = init_pos_limit
        self.cart_coef = WindowWidth / init_pos_limit
        self.simulation.set_simulation_parameters(sheep_move_dist=sheep_move_dist, wolf_move_dist=wolf_move_dist)

    def __init__(self, sheep_move_dist, wolf_move_dist, init_pos_limit, parent=None):
        super(MainLogicThread, self).__init__(parent=parent)
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.init_pos_limit = init_pos_limit
        self.cart_coef = WindowWidth / init_pos_limit

        self.simulation = playground.Simulation(sheep_move_dist=sheep_move_dist,
                                                wolf_move_dist=wolf_move_dist)

    def add_sheep(self, position: Point):
        self.simulation.create_sheep(self.convert_from_cartesian(position))
        res = []
        temp_pos = self.simulation.get_alive_sheep_positions()
        for i in range(len(temp_pos)):
            res.append(self.convert_to_cartesian(copy.copy(temp_pos[i])))
        return res

    def change_wolf_position(self, position: Point):
        self.simulation.change_wolf_position((self.convert_from_cartesian(position)))
        return self.convert_to_cartesian(copy.copy(self.simulation.playground.wolf.position))

    def get_sheep_positions(self):
        res = []
        temp_pos = self.simulation.get_alive_sheep_positions()
        for i in range(len(temp_pos)):
            res.append(self.convert_to_cartesian(copy.copy(temp_pos[i])))
        return res

    def get_wolf_position(self):
        return self.convert_to_cartesian(copy.copy(self.simulation.playground.wolf.position))

    def run_round(self):
        self.simulation.run_round(self.simulation.round_counter)

    def reset(self):
        self.simulation.remove_sheep()
        self.simulation.change_wolf_position(Point(0, 0))

    def convert_to_cartesian(self, point):
        point.x = int((point.x + 5) * self.cart_coef)
        point.y = int((point.y + 5) * self.cart_coef)
        return point

    def convert_from_cartesian(self, point):
        point.x = (point.x / self.cart_coef) - 5  # can't be casted to int
        point.y = (point.y / self.cart_coef) - 5  # can't be casted to int
        return point

    def run(self):
        self.element_signal.emit([Point(1, 1)])

    def stop(self):
        self.terminate()


class MainWindow(QMainWindow):
    wer = WindowWidth / 10  # wolf ellipse radius
    ser = wer * 0.6  # wolf ellipse radius, 60%
    init_pos_limit = wer / 5
    wolf_move_dist = init_pos_limit * 0.1
    sheep_move_dist = wolf_move_dist / 2
    cartesian_zero = Point(WindowWidth // 2, WindowWidth // 2)  # suppose that height = width
    sheep_color = Qt.green
    wolf_color = Qt.red

    sheep_positions = []  # points to be drawn

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        self.mainLogicThread = MainLogicThread(sheep_move_dist=self.sheep_move_dist, wolf_move_dist=self.wolf_move_dist,
                                               init_pos_limit=self.init_pos_limit)

        self.mainLogicThread.element_signal.connect(self.update_draw_elements)
        self.wolf_position = self.mainLogicThread.change_wolf_position(copy.copy(self.cartesian_zero))
        self._set_configuration()
        # self.mainLogicThread.start()
        self.UiComponents()
        self.show()

    def UiComponents(self):
        step_btn = QPushButton("step", self)
        step_btn.setGeometry(0, 25, 100, 30)
        step_btn.clicked.connect(self.step_button_click)

        reset_btn = QPushButton("reset", self)
        reset_btn.setGeometry(105, 25, 100, 30)
        reset_btn.clicked.connect(self.reset_button_click)

        self.sheep_number_label = QLabel("sheep: 15", self)
        self.sheep_number_label.setGeometry(210, 25, 100, 30)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(4)
        self.slider.setTickInterval(1)
        self.slider.setValue(2)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setGeometry(305, 25, 100, 30)
        self.slider.valueChanged.connect(self.change_scale)

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')

        open_action = QAction("Open", self)
        # open_action.triggered.connect() #todo
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        # save_action.triggered.connect() # todo
        file_menu.addAction(save_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        settings_menu = main_menu.addMenu('Settings')

        wolf_color_action = QAction("Wolf color", self)
        wolf_color_action.triggered.connect(self.pick_wolf_color)
        settings_menu.addAction(wolf_color_action)

        sheep_color_action = QAction("Sheep color", self)
        sheep_color_action.triggered.connect(self.pick_sheep_color)
        settings_menu.addAction(sheep_color_action)

        background_color_action = QAction("Background color", self)
        background_color_action.triggered.connect(self.pick_background_color)
        settings_menu.addAction(background_color_action)

        # self.setStyleSheet("QMainWindow {background: 'cyan';}")

    def pick_background_color(self):
        color = QColorDialog.getColor()
        self.setStyleSheet("QMainWindow { background-color: %s}" % color.name())

    def pick_wolf_color(self):
        self.wolf_color = QColorDialog.getColor()
        self.update()

    def pick_sheep_color(self):
        self.sheep_color = QColorDialog.getColor()
        self.update()

    def reset_button_click(self):
        self.mainLogicThread.reset()
        self.sheep_positions = self.mainLogicThread.get_sheep_positions()
        self.wolf_position = self.mainLogicThread.get_wolf_position()
        self.update()

        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        # msg.setWindowTitle("Information")
        # msg.setText("Last sheep has been eaten")
        # x = msg.exec_()

    def step_button_click(self):
        if len(self.sheep_positions) != 0:
            self.mainLogicThread.run_round()
            self.sheep_positions = self.mainLogicThread.get_sheep_positions()
            self.wolf_position = self.mainLogicThread.get_wolf_position()
            self.update()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
            msg.setText("There is no sheep on the field.")
            x = msg.exec_()

    def _set_configuration(self):
        self.setAutoFillBackground(True)
        self.setGeometry(0, 0, WindowWidth, WindowWidth)  # suppose that height = width
        self.setWindowTitle("WolfAgainstSheep - simulation")

    def closeEvent(self, event):
        super(MainWindow, self).closeEvent(event)
        # self.mainLogicThread.stop()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for e in self.sheep_positions:
            temp_1 = e.x - self.ser // 2
            temp_2 = e.y - self.ser // 2
            painter.setPen(QPen(Qt.black, 12, Qt.SolidLine))
            painter.setBrush(QBrush(self.sheep_color, Qt.SolidPattern))
            painter.drawEllipse(int(temp_1), int(temp_2), int(self.ser), int(self.ser))

        temp_1 = self.wolf_position.x - self.wer // 2
        temp_2 = self.wolf_position.y - self.wer // 2
        painter.setPen(QPen(Qt.black, 12, Qt.SolidLine))
        painter.setBrush(QBrush(self.wolf_color, Qt.SolidPattern))
        painter.drawEllipse(int(temp_1), int(temp_2), int(self.wer), int(self.wer))

        self.sheep_number_label.setText("sheep: " + str(len(self.sheep_positions)))

    def change_scale(self):
        # WindowWidth = 250
        WindowWidth = self.slider.value()*125+250
        self.wer = WindowWidth / 10  # wolf ellipse radius
        self.ser = self.wer * 0.6  # wolf ellipse radius, 60%
        self.init_pos_limit = self.wer / 5
        self.wolf_move_dist = self.init_pos_limit * 0.1
        self.sheep_move_dist = self.wolf_move_dist / 2
        self.cartesian_zero = Point(WindowWidth // 2, WindowWidth // 2)  # suppose that height = width
        self.mainLogicThread.set_simulation_parameters(self.sheep_move_dist, self.wolf_move_dist, self.init_pos_limit,
                                                       WindowWidth)
        self.update()

    def update_draw_elements(self, elements):
        self.sheep_positions = elements
        self.update()

    def update_wolf_position(self, position):
        self.wolf_position = self.mainLogicThread.change_wolf_position(position)
        self.update()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.RightButton:
            self.update_wolf_position(Point(QMouseEvent.pos().x(), QMouseEvent.pos().y()))

        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.update_draw_elements(
                self.mainLogicThread.add_sheep(Point(x=QMouseEvent.pos().x(), y=QMouseEvent.pos().y())))


myApp = QApplication(sys.argv)
myApp.setWindowIcon(QIcon("resources/wolf.png"))
window = MainWindow()
myApp.exec_()
sys.exit()
