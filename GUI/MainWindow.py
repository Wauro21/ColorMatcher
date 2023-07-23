from GUI.CentralWidget import CentralWidget
from GUI.Constants import MAIN_WINDOW_TITLE
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
import sys
import os

class ColorMatcherMain(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        # objects

        # widgets
        self.DeLoreanWidget = CentralWidget(self)

        # init routines
        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setCentralWidget(self.DeLoreanWidget)
        self.setWindowIcon(QtGui.QIcon('rsrcs/icon.png'))

        # signals and slots

        # layout


if __name__ == '__main__':

    app = QApplication([])
    if os.name == 'nt':
        app.setStyle('Fusion')
    window = ColorMatcherMain()
    window.show()
    sys.exit(app.exec_())