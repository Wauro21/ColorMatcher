from GUI.Constants import IMAGE_FILE_FIELD_LABEL, IMAGE_HOLDER_MIME_TYPES, IMAGE_WINDOW_TITLE_FILEDIALOG, PORTRAIT_MIN_DIMS, REFERENCE_IMAGE_TITLE
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QSizePolicy, QGroupBox
from PySide2.QtGui import QPixmap, QColor, QPainter, QImage
from PySide2.QtCore import Signal, Slot, Qt
import sys
import os
import cv2
import numpy as np
from GUI.PortraitWidget import PortraitWidget

class ColorPicker(QWidget):

    pick_roi = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects
         
        #Widgets
        self.pick_btn = QPushButton('ROI', self)
        self.color_label = QLabel(self)
        self.color_name = QLabel('Color Value: #------', self)
        self.color = []

        # init routines
        self.initColorLabel()

        # Slots and Signals
        self.pick_btn.clicked.connect(self.askROI)

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.pick_btn)
        layout.addStretch(1)
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_name)
        
        self.setLayout(layout)

    def reset(self):

        # Reset value
        self.color = []

        # Reset color label
        self.initColorLabel()

        # Reset text 
        self.color_name.setText('Color Value: #------')

    def initColorLabel(self):
        pix = QPixmap('rsrcs/color_picker_icon.png')
        pix = pix.scaled(20,20)
        self.color_label.setPixmap(pix)


    def askROI(self):
        self.pick_roi.emit()

    def updateColorName(self, color_hex):
        self.color_name.setText('Color Value: {}'.format(color_hex))


    def processROI(self, roi):
        avg_color = np.average(roi, axis=(0,1))
        rounded_avg = np.around(avg_color)

        self.color = rounded_avg

        # Falta color aca
        color_pixmap = QPixmap(20,20)
        
        hex_color = self.rgb2hex(rounded_avg)
        self.updateColorName(hex_color)
        color_pixmap.fill(QColor(hex_color))
        self.color_label.setPixmap(color_pixmap)

    def rgb2hex(self, rgb):
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])

        return '#{:02x}{:02x}{:02x}'.format(r,g,b)


class ImageButtons(QWidget):

    loaded_path = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects 

        # Widgets
        self.file_label = QLabel('Archivo:',self)
        self.file_field = QLineEdit(IMAGE_FILE_FIELD_LABEL, self)
        self.load_button = QPushButton('Cargar', self)

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
        self.roi_ready = False

        # Widgets
        self.group_box = QGroupBox(title, self)
        self.frame = PortraitWidget(PORTRAIT_MIN_DIMS,self)
        self.load_ctrl = ImageButtons(self)
        self.color_picker = ColorPicker(self)

        # Init Routines

        self.group_box.setStyleSheet(
            '''
            QGroupBox { 
                font-weight: bold;
                font-size: 15px;
            }
            '''
        )

        # Signals and Slots
        self.load_ctrl.loaded_path.connect(self.loadedImg)
        self.color_picker.pick_roi.connect(self.frame.enableROI)
        self.frame.roi.connect(self.receiveROI)

        # Layout
        layout = QVBoxLayout()

        # Group layout
        group = QVBoxLayout()
        group.addWidget(self.load_ctrl)
        group.addWidget(self.frame)
        group.addWidget(self.color_picker)

        self.group_box.setLayout(group)

        layout.addWidget(self.group_box)

        self.setLayout(layout)

    def receiveROI(self, roi):
        self.color_picker.processROI(roi)
        self.roi_ready = True

    def loadedImg(self, path):
        self.frame.updateViewer(path)
        self.color_picker.reset()
        self.frame.resetROI()
        self.roi_ready = False

    def roiReady(self):
        return self.roi_ready


    def getColor(self):
        return self.color_picker.color



if __name__ == '__main__':
    app = QApplication([])
    test = ImageViewer('Primera imagen', 'primera descripcion')
    test.show()
    sys.exit(app.exec_())