from GUI.Constants import IMAGE_FILE_FIELD_LABEL, IMAGE_HOLDER_MIME_TYPES, IMAGE_WINDOW_TITLE_FILEDIALOG, PORTRAIT_MIN_DIMS
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QSizePolicy
from PySide2.QtGui import QPixmap, QColor, QPainter, QImage
from PySide2.QtCore import Signal, Slot, Qt
import sys
import os
import cv2
import numpy as np
from GUI.PortraitWidget import PortraitWidget

class ImageButtons(QWidget):

    loaded_path = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects 

        # Widgets
        self.file_label = QLabel('File:',self)
        self.file_field = QLineEdit(IMAGE_FILE_FIELD_LABEL, self)
        self.load_button = QPushButton('Load', self)

        # init routines

        self.file_label.setStyleSheet(
            'font-weight:bold'
        )

        self.file_field.setReadOnly(True)

        # Signals and Slots
        self.load_button.clicked.connect(self.loadImg)

        # layouts
        layout = QHBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_field)
        layout.addWidget(self.load_button)
        self.setLayout(layout)


    def loadImg(self):
        fileDialog = QFileDialog(self, windowTitle=IMAGE_WINDOW_TITLE_FILEDIALOG)
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setMimeTypeFilters(IMAGE_HOLDER_MIME_TYPES)

        if fileDialog.exec_():
            files = fileDialog.selectedFiles()
            # Update file field
            self.file_field.setText(files[0])

            # Emit signal to update frame 
            self.loaded_path.emit(files[0])



class ImageViewer(QWidget):

    def __init__(self, title, desc, parent=None):
        super().__init__(parent)

        # Objects 
        self.frame_path = None
        self.pix_map = None

        # Widgets
        self.title = QLabel(title, self)
        self.description = QLabel(desc, self)
        self.frame = PortraitWidget(PORTRAIT_MIN_DIMS,self)
        self.load_ctrl = ImageButtons(self)

        # Init Routines
        self.description.setWordWrap(True)

        self.description.setAlignment(Qt.AlignCenter)

        self.title.setStyleSheet(
            '''
            font-weight:bold;
            font-size: 20px;
            '''
        )

        self.description.setStyleSheet(
            '''
            font-size: 15px;
            '''
        )

        # Signals and Slots
        self.load_ctrl.loaded_path.connect(self.frame.updateViewer)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addWidget(self.frame)
        layout.addStretch(1)
        layout.addWidget(self.load_ctrl)
        layout.addStretch(1)
        self.setLayout(layout)

class ImageResult(QWidget):
    def __init__(self, title, desc, parent=None):
        super().__init__(parent)

        # Objects 
        self.frame_path = None
        self.pix_map = None

        # Widgets
        self.title = QLabel(title, self)
        self.description = QLabel(desc, self)
        self.frame = PortraitWidget(PORTRAIT_MIN_DIMS,self)
        self.process_btn = QPushButton('Process')

        # Init Routines
        self.description.setWordWrap(True)

        self.description.setAlignment(Qt.AlignCenter)

        self.title.setStyleSheet(
            '''
            font-weight:bold;
            font-size: 20px;
            '''
        )

        self.description.setStyleSheet(
            '''
            font-size: 15px;
            '''
        )

        # Signals and Slots
        self.process_btn.clicked.connect(lambda: print('Process button'))

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addWidget(self.frame)
        layout.addStretch(1)
        layout.addWidget(self.process_btn)
        layout.addStretch(1)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    test = ImageViewer('Primera imagen', 'primera descripcion')
    test.show()
    sys.exit(app.exec_())