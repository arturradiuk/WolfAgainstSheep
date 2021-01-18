import copy
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter, QIcon, QBrush, QPen, QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox, QLabel, QSlider, QAction,
                             QColorDialog, QFileDialog, QWidget, QButtonGroup, QRadioButton)
import json
import playground
from model.point_model import Point

WindowWidth = 500
WindowHeight = WindowWidth  # suppose that height = width


class MainLogicThread(QThread):
    update_state = pyqtSignal()
    delay = 1.0

    stopper = False

    def set_simulation_parameters(self, sheep_move_dist, wolf_move_dist, init_pos_limit, window_width):
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.init_pos_limit = init_pos_limit
        self.cart_coef = window_width / init_pos_limit
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
        res = Point()
        res.x = int((point.x + 5) * self.cart_coef)
        res.y = int((point.y + 5) * self.cart_coef)
        return res

    def convert_from_cartesian(self, point):
        res = Point()
        res.x = (point.x / self.cart_coef) - 5  # can't be casted to int
        res.y = (point.y / self.cart_coef) - 5  # can't be casted to int
        return res

    def run(self):
        while len(self.get_sheep_positions()) != 0 and (not self.stopper):
            time.sleep(self.delay)
            self.simulation.run_round(self.simulation.round_counter)
            self.update_state.emit()

    def stop(self):
        self.stopper = True


class MainWindow(QMainWindow):
    wer = WindowWidth / 10  # wolf ellipse radius
    ser = wer * 0.6  # wolf ellipse radius, 60%
    init_pos_limit = wer / 5
    wolf_move_dist = init_pos_limit * 0.1
    sheep_move_dist = wolf_move_dist / 2
    cartesian_zero = Point(WindowWidth // 2, WindowWidth // 2)  # suppose that height = width
    sheep_color = QColor(6, 255, 68)
    wolf_color = QColor(255, 0, 101)
    active_click = True

    sheep_positions = []  # points to be drawn

    def update_signal_handler(self):
        self.wolf_position = self.mainLogicThread.get_wolf_position()
        self.sheep_positions = self.mainLogicThread.get_sheep_positions()
        self.update()

        if len(self.sheep_positions) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Information")
            msg.setText("Last sheep has been eaten")
            x = msg.exec_()
            self.start_stop_btn_action(True)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        self.mainLogicThread = MainLogicThread(sheep_move_dist=self.sheep_move_dist, wolf_move_dist=self.wolf_move_dist,
                                               init_pos_limit=self.init_pos_limit)

        self.mainLogicThread.update_state.connect(self.update_signal_handler)

        self.wolf_position = self.mainLogicThread.change_wolf_position(copy.copy(self.cartesian_zero))
        self._set_configuration()
        self.ui_component_conf()
        self.show()

    def start_stop_btn_action(self, par=False):
        if self.start_stop_btn.text() == "Start" and not (par) and not len(self.sheep_positions) == 0:
            self.start_stop_btn.setText("Stop")
            self.mainLogicThread.stopper = False
            self.mainLogicThread.start()

            self.reset_btn.setEnabled(False)
            self.step_btn.setEnabled(False)
            self.slider.setEnabled(False)
            self.menuBar().setEnabled(False)
            self.active_click = False

        else:
            self.start_stop_btn.setText("Start")
            self.mainLogicThread.stop()

            self.reset_btn.setEnabled(True)
            self.step_btn.setEnabled(True)
            self.slider.setEnabled(True)
            self.menuBar().setEnabled(True)
            self.active_click = True

    def ui_component_conf(self):
        self.step_btn = QPushButton("step", self)
        self.step_btn.setGeometry(0, 25, 100, 30)
        self.step_btn.clicked.connect(self.step_button_click)

        self.reset_btn = QPushButton("reset", self)
        self.reset_btn.setGeometry(105, 25, 100, 30)
        self.reset_btn.clicked.connect(self.reset_button_click)

        self.sheep_number_label = QLabel("sheep: 15", self)
        self.sheep_number_label.setGeometry(210, 25, 100, 30)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(4)
        self.slider.setTickInterval(1)
        self.slider.setValue(2)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setGeometry(285, 25, 100, 30)
        self.slider.valueChanged.connect(self.change_scale)

        self.start_stop_btn = QPushButton("Start", self)
        self.start_stop_btn.setGeometry(390, 25, 100, 30)
        self.start_stop_btn.clicked.connect(self.start_stop_btn_action)

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.file_open)  # todo
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.file_save)  # todo
        file_menu.addAction(save_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.run_settings)
        main_menu.addAction(settings_action)

    def run_settings(self):
        self.settings_window = QWidget()
        self.settings_window.setGeometry(100, 100, 200, 200)

        change_wolf_color_btn = QPushButton("change wolf color", self.settings_window)
        change_wolf_color_btn.setGeometry(10, 10, 180, 25)
        change_wolf_color_btn.clicked.connect(self.pick_wolf_color)

        sheep_color_action_btn = QPushButton("change sheep color", self.settings_window)
        sheep_color_action_btn.setGeometry(10, 40, 180, 25)
        sheep_color_action_btn.clicked.connect(self.pick_sheep_color)

        background_color_btn = QPushButton("change background color", self.settings_window)
        background_color_btn.setGeometry(10, 70, 180, 25)
        background_color_btn.clicked.connect(self.pick_background_color)

        radio_buttons = []

        def radio_button_toggle():
            for i in range(4):
                if radio_buttons[i].isChecked():
                    self.mainLogicThread.delay = float(radio_buttons[i].text())
                    break

        radio_buttons.append(QRadioButton("0.5", self.settings_window))
        radio_buttons[0].setGeometry(10, 100, 180, 25)
        radio_buttons[0].clicked.connect(radio_button_toggle)

        radio_buttons.append(QRadioButton("1.0", self.settings_window))
        radio_buttons[1].setGeometry(10, 120, 180, 25)
        radio_buttons[1].clicked.connect(radio_button_toggle)

        radio_buttons.append(QRadioButton("1.5", self.settings_window))
        radio_buttons[2].setGeometry(10, 140, 180, 25)
        radio_buttons[2].clicked.connect(radio_button_toggle)

        radio_buttons.append(QRadioButton("2.0", self.settings_window))
        radio_buttons[3].setGeometry(10, 160, 180, 25)
        radio_buttons[3].clicked.connect(radio_button_toggle)

        for i in range(4):
            if str(self.mainLogicThread.delay) == radio_buttons[i].text():
                radio_buttons[i].setChecked(True)
                break

        self.settings_window.show()

    def pick_background_color(self):
        color = QColorDialog.getColor()
        self.setStyleSheet("QMainWindow { background-color: %s}" % color.name())
        if hasattr(self, 'settings_window'):
            self.settings_window.hide()

    def pick_wolf_color(self):
        self.wolf_color = QColorDialog.getColor()
        if hasattr(self, 'settings_window'):
            self.settings_window.hide()
        self.update()

    def pick_sheep_color(self):
        self.sheep_color = QColorDialog.getColor()
        if hasattr(self, 'settings_window'):
            self.settings_window.hide()
        self.update()

    def reset_button_click(self):
        self.mainLogicThread.reset()
        self.sheep_positions = self.mainLogicThread.get_sheep_positions()
        self.wolf_position = self.mainLogicThread.get_wolf_position()
        self.update()

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
        if hasattr(self, 'settings_window'):
            self.settings_window.hide()

    def file_open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            self.read_simulation_conf_info(fileName=fileName)

    def read_simulation_conf_info(self, fileName):
        f = open(fileName, )
        simulation_conf = json.load(f)
        self.mainLogicThread.reset()  #

        temp_wolf_position = Point(simulation_conf['wolf_position'][0], simulation_conf['wolf_position'][1])
        temp_wolf_position = self.mainLogicThread.convert_to_cartesian(temp_wolf_position)
        self.mainLogicThread.change_wolf_position(temp_wolf_position)

        for s in simulation_conf['sheep']:
            temp_sheep = Point(s[0], s[1])
            temp_sheep = self.mainLogicThread.convert_to_cartesian(temp_sheep)
            self.mainLogicThread.add_sheep(temp_sheep)

        self.wolf_position = self.mainLogicThread.get_wolf_position()
        self.sheep_positions = self.mainLogicThread.get_sheep_positions()

        self.slider.setValue(simulation_conf['scale'])
        self.change_scale()

        self.mainLogicThread.delay = simulation_conf['delay']

        self.sheep_color = QColor(simulation_conf['sheep_color'])
        self.wolf_color = QColor(simulation_conf['wolf_color'])
        self.setStyleSheet("QMainWindow { background-color: %s}" % QColor(simulation_conf['background_color']).name())
        self.update()

    def file_save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            self.write_simulation_conf_info(file_name=fileName)

    def write_simulation_conf_info(self, file_name):
        simulation_conf = {}
        simulation_conf.update({'sheep_color': self.sheep_color.name()})
        simulation_conf.update({'wolf_color': self.wolf_color.name()})
        simulation_conf.update({'background_color': self.palette().color(QPalette.Background).name()})

        simulation_conf.update({'scale': self.slider.value()})
        simulation_conf.update({'delay': self.mainLogicThread.delay})

        temp_wolf = self.mainLogicThread.convert_from_cartesian(self.wolf_position)
        simulation_conf.update({'wolf_position': [temp_wolf.x, temp_wolf.y]})
        sheep = []

        for s in self.sheep_positions:
            temp_sheep = self.mainLogicThread.convert_from_cartesian(s)
            sheep.append([temp_sheep.x, temp_sheep.y])

        simulation_conf.update({'sheep': sheep})
        simulation_conf = json.dumps(simulation_conf)
        with open(file_name, 'w') as outfile:
            outfile.write(simulation_conf)

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
        WindowWidth = self.slider.value() * 125 + 250
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
        if self.active_click:
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
