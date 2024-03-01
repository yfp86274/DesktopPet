# image_widget.py
import configparser
import random

from PyQt6.QtCore import QTimer, Qt, QPoint, QProcess
from PyQt6.QtGui import QMouseEvent, QAction
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QMenu


class ImageWidget(QWidget):
    def __init__(self, actions, config_file):
        super().__init__()
        self.setWindowTitle('PyQt6')
        self.setGeometry(100, 100, 128, 128)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background:transparent")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.layout.addWidget(self.label)

        self.actions = actions
        self.current_action = random.choice(self.actions)

        self.image_timer = QTimer(self)
        self.image_timer.timeout.connect(self.next_image)
        self.image_timer.start(self.current_action.interval)

        self.action_timer = QTimer(self)
        self.action_timer.timeout.connect(self.next_action)
        self.action_timer.start(self.current_action.duration)

        self.oldPos = self.pos()

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def next_image(self):
        self.label.setPixmap(next(self.current_action.image_cycle))

    def next_action(self):
        self.current_action = random.choice(self.actions)
        self.image_timer.start(self.current_action.interval)
        self.action_timer.start(self.current_action.duration)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            self.showContextMenu(event)
        else:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def showContextMenu(self, event):
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet("""
            QMenu {
                background-color: white; 
                color: black;
            }
            QMenu::item:selected {
                background-color: lightblue;
            }
        """)  # set menu style

        for section in self.config.sections():
            for key in self.config[section]:
                action = self.createAction(key, self.config[section][key])  # use the new method here
                contextMenu.addAction(action)

        quitAct = QAction("Quit", self)
        quitAct.triggered.connect(self.close)
        contextMenu.addAction(quitAct)

        contextMenu.exec(event.globalPosition().toPoint())

    def createAction(self, name, command):  # add this method
        action = QAction(name, self)
        action.triggered.connect(lambda: QProcess.startDetached(command))
        return action
