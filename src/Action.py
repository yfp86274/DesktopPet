# Action.py
import json
from itertools import cycle

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class Action:
    def __init__(self, images, duration, interval, speeds):
        self.image_cycle = cycle(QPixmap(fname).scaled(128, 128, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation) for fname in images)
        self.duration = duration
        self.interval = interval
        self.speeds = cycle(speeds)  # speeds is now a list of speed objects

    @staticmethod
    def load_actions_from_file(filename):
        with open(filename) as f:
            actions_data = json.load(f)
        return {name: Action(**data) for name, data in actions_data.items()}  # 修改這行

    @staticmethod
    def load_sequences_from_file(filename):
        with open(filename) as f:
            sequences_data = json.load(f)
        return sequences_data
