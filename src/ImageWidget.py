import configparser
import random

from PyQt6.QtCore import QTimer, Qt, QPoint, QProcess
from PyQt6.QtGui import QMouseEvent, QAction, QGuiApplication
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QMenu


class ImageWidget(QWidget):
    def __init__(self, actions, sequences, config_file):
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
        self.sequences = sequences
        self.current_sequence_name = 'normal'  # 默認的序列名稱
        self.current_action_index = 0
        self.current_action = self.get_random_action_from_sequence(self.sequences[self.current_sequence_name])  # 默認序列隨機
        self.current_speed = next(self.current_action.speeds)

        self.image_timer = QTimer(self)
        self.image_timer.timeout.connect(self.next_image)
        self.image_timer.start(self.current_action.interval)

        self.action_timer = QTimer(self)
        self.action_timer.timeout.connect(self.next_action)
        self.action_timer.start(self.current_action.duration)

        self.speed_timer = QTimer(self)  # new timer for changing the speed
        self.speed_timer.timeout.connect(self.next_speed)
        self.speed_timer.start(self.current_speed['duration'])

        self.move_timer = QTimer(self)  # new timer for moving the window
        self.move_timer.timeout.connect(self.move_window)
        self.move_timer.start(100)  # update the window position every 100 ms

        self.oldPos = self.pos()

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def next_image(self):
        self.label.setPixmap(next(self.current_action.image_cycle))

    def next_action(self):
        sequence = self.sequences[self.current_sequence_name]
        if sequence['mode'] == 'sequential':
            self.current_action_index = (self.current_action_index + 1) % len(sequence['actions'])
            if self.current_action_index == 0:  # 如果已經播放完畢
                self.current_sequence_name = sequence.get('next', self.current_sequence_name)  # 切換到下一個序列
        elif sequence['mode'] == 'random':
            self.current_action_index = random.randint(0, len(sequence['actions']) - 1)
        action_name = sequence['actions'][self.current_action_index]
        self.current_action = self.actions[action_name]
        self.image_timer.start(self.current_action.interval)
        self.action_timer.start(self.current_action.duration)
        self.current_speed = next(self.current_action.speeds)
        self.speed_timer.start(self.current_speed['duration'])

    def get_random_action_from_sequence(self, sequence):
        action_names = sequence['actions']
        action_objects = [self.actions[name] for name in action_names]
        return random.choice(action_objects)

    def set_sequence_by_name(self, name):
        self.current_sequence_name = name
        self.next_action()

    def next_speed(self):
        self.current_speed = next(self.current_action.speeds)
        self.speed_timer.start(self.current_speed['duration'])

    def move_window(self):
        # Get the current position and screen size
        pos = self.pos()
        screen = QGuiApplication.primaryScreen()
        rect = screen.availableGeometry()

        # Calculate the new position
        newPos = pos + QPoint(*self.current_speed['speed'])

        # Check if the new position is within the screen bounds
        if rect.contains(newPos):
            self.move(newPos)

    def mousePressEvent(self, event: QMouseEvent):  # 滑鼠點擊事件
        if event.button() == Qt.MouseButton.RightButton:
            self.showContextMenu(event)
        else:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):  # 滑鼠移動事件
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent):  # 滑鼠放開事件
        self.set_sequence_by_name("mouseRelease")

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
