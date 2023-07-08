import sys
import os
from GUI.MainWindow import DeLoreanMain
from PySide2.QtWidgets import QApplication



if __name__ == '__main__':

    app = QApplication([])
    if os.name == 'nt':
        app.setStyle('Fusion')
    window = DeLoreanMain()
    window.show()
    sys.exit(app.exec_())