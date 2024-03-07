# Main.py
import sys

from PyQt6.QtWidgets import QApplication

from Action import Action
from ImageWidget import ImageWidget


def main():
    app = QApplication(sys.argv)
    actions = Action.load_actions_from_file('../config/actions.json')
    sequences = Action.load_sequences_from_file('../config/sequences.json')
    window = ImageWidget(actions, sequences, "../config/menu.txt")
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
