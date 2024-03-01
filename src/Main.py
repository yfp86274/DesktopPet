# main.py
import sys

from PyQt6.QtWidgets import QApplication

from Action import Action
from ImageWidget import ImageWidget


def main():
    app = QApplication(sys.argv)
    actions = Action.load_from_file('../config/actions.json')
    window = ImageWidget(actions, "../config/menu.txt")
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
