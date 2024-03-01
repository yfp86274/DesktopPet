# action.py
import json
from itertools import cycle

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class Action:
    def __init__(self, name, images, duration, interval):
        self.name = name
        self.image_cycle = cycle(QPixmap(fname).scaled(128, 128, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation) for fname in images)
        self.duration = duration
        self.interval = interval

    @staticmethod
    def load_from_file(filename):
        with open(filename) as f:
            actions_data = json.load(f)
        return [Action(**action_data) for action_data in actions_data['actions']]
