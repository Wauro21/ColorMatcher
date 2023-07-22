from GUI.Constants import PORTRAIT_DEFAULT_BG_COLOR
from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtGui import QPixmap, QColor, QPainter, QImage
from PySide2.QtCore import Signal, Slot, Qt
import cv2
import numpy as np

import matplotlib.pyplot as plt



class PortraitWidget(QLabel):
    roi = Signal(np.ndarray)

    def __init__(self, min_size, parent=None):
        super().__init__(parent)

        # Objects 
        self.min_size = min_size
        self.image = None
        self.image_resized = None
        self.pix_map = QPixmap()
        self.roi_enabled = False

        # -> roi coordinates
        self.start = None
        self.end = None

        # init routine
        # -> Enable vertical grow
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.setSizePolicy(size_policy)
        self.initViewer()
        # -> Set minimum size
        w, h = self.min_size
        self.setMinimumSize(w, h)

        # -> Mouse position
        self.setMouseTracking(True)
        self.mousePressEvent = self.pickROI
        self.mouseReleaseEvent = self.releaseROI


    def enableROI(self):
        if(self.image is not None):
            self.roi_enabled = True


    def releaseROI(self, event):
        if(self.roi_enabled):
            self.roi_enabled = False
            
            # Unpack coordinates

            x_i = self.start[0]
            y_i = self.start[1]
            x_e = self.end[0]
            y_e = self.end[1]

            # Convert to original coordinates
            # -> Get conv factors
            try: 
                h, w, ch = self.image.shape
                hp, wp, chp = self.image_resized.shape
            except:
                h, w = self.image.shape
                ch = None
                hp, wp = self.image_resized.shape
                chp = None

            conv_x = h/hp
            conv_y = w/wp

            # -> coordinates in original image
            x_start = round(x_i*conv_x)
            x_end = round(x_e*conv_x)
            y_start = round(y_i*conv_y)
            y_end = round(y_e*conv_y)
            
            # Get roi
            selection = self.image[y_start:y_end, x_start:x_end]
            self.roi.emit(selection)

    def pickROI(self, event):
        if(self.roi_enabled):
            x = event.pos().x()
            y = event.pos().y()
            self.start = [x, y]

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton & self.roi_enabled:
            x = event.pos().x()
            y = event.pos().y()

            # Check if inside limits
            if(x > self.width()): x = self.width()
            if(x < 0): x = 0
            if(y > self.height()): y = self.height()
            if(y < 0): y = 0

            self.end = [x, y]

            self.update()


    def setPixmap(self, pix):
        self.pix_map = pix
        self.update()

    def paintEvent(self, event):
        print('paint event | roi {}'.format(self.roi_enabled))
        if not self.pix_map.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            # Check if there is an image
            if self.image is not None:
                self.resizeFrame()

                if(self.roi_enabled):
                    self.image_resized = cv2.rectangle(self.image_resized, self.start, self.end, (255,0,0), 2)
                    

                self.pix_map = self.convert2Pixmap()
            painter.drawPixmap(0,0, self.width(), self.height(), self.pix_map)

    def initViewer(self):
        w, h = self.min_size
        gray_fill = QPixmap(w, h)
        gray_fill.fill(QColor(PORTRAIT_DEFAULT_BG_COLOR))
        self.setPixmap(gray_fill)

    def convert2Pixmap(self):
        h, w, ch = self.image_resized.shape
        bytes_per_line = ch*w
        converted = QImage(self.image_resized, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(converted)

    def updateViewer(self, img_path):
        # Load image
        self.image = cv2.imread(img_path, -1)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # Resize to widget size adding padding if necessary
        self.resizeFrame()
        self.setPixmap(self.convert2Pixmap())

    def resizeFrame(self):
        try: 
            h, w, ch = self.image.shape
        except:
            h, w = self.image.shape
            ch = None
        # Get aspect ratio
        ar = w/h

        # Target dimensions
        H = self.height()
        W = self.width()
        AR = W/H # Target aspect ratio

        # -> Fix height
        nH = H
        # -> From aspect ratio get new width
        nW = round(ar*nH)

        while(nW > W):
            nH -= 10
            nW = round(ar*nH)
        # Apply resizing with the possible dimensions
        resized_frame = cv2.resize(self.image, (nW, nH))

        # Generate final target size and fill with black color
        if(ch):
            f_frame = np.zeros((H, W, ch), np.uint8)
        else:
            f_frame = np.zeros((H, W), np.uint8)

        # Position resized frame inside final frame
        aH, aW = (H-nH)//2, (W-nW)//2
        f_frame[aH:aH+nH, aW:aW+nW] = resized_frame

        self.image_resized = f_frame