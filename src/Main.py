import configparser
import sys
from itertools import cycle

from PyQt6.QtCore import QTimer, Qt, QPoint, QProcess
from PyQt6.QtGui import QPixmap, QMouseEvent, QAction
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMenu


class ImageWidget(QWidget):
    def __init__(self, image_files, interval=100):  # change interval to 100 ms
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

        self.image_cycle = cycle(QPixmap(fname).scaled(128, 128, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation) for fname in
                                 image_files)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)
        self.timer.start(interval)

        self.oldPos = self.pos()

        self.config = configparser.ConfigParser()
        self.config.read('../config/config.txt')

    def next_image(self):
        self.label.setPixmap(next(self.image_cycle))

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
        contextMenu.setStyleSheet("background-color: white; color: black;")  # set menu style

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


def main():
    app = QApplication(sys.argv)
    image_files = [f'../images/shime{i}.png' for i in range(1, 7)]
    window = ImageWidget(image_files)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
