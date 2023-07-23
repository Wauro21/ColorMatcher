from GUI.Constants import PORTARIT_ROI_COLOR, PORTRAIT_DEFAULT_BG_COLOR
from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtGui import QPixmap, QColor, QPainter, QImage
from PySide2.QtCore import Signal, Slot, Qt
import cv2
import numpy as np


class PortraitWidget(QLabel):
    roi = Signal(np.ndarray)

    def __init__(self, min_size, parent=None):
        super().__init__(parent)

        # Objects 
        self.min_size = min_size
        self.image = None # Original image
        self.image_rescaled = None # Factible image with desired dims
        self.image_resized = None  # Req image composited
        self.pix_map = QPixmap()
        
        # -> roi
        self.roi_enabled = False
        self.start = None
        self.end = None
        self.offset = [0, 0]

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

    def resetROI(self):
        self.roi_enabled = False
        self.start = None
        self.end = None

    def getImageShape(self, image):
        try: 
            h, w, ch = image.shape
        except:
            h, w = image.shape
            ch = None

        return h, w, ch


    def enableROI(self):
        if(self.image is not None):
            self.roi_enabled = True
            self.setCursor(Qt.CrossCursor)


    def releaseROI(self, event):
        if(self.roi_enabled):
            self.roi_enabled = False
            self.setCursor(Qt.ArrowCursor)
            
            # Unpack coordinates

            x_i = min(self.start[0], self.end[0])
            y_i = min(self.start[1], self.end[1])
            x_e = max(self.start[0], self.end[0])
            y_e = max(self.start[1], self.end[1])

            # Convert to original coordinates
            # -> Get conv factors
            h, w, ch = self.getImageShape(self.image)

            conv_x = w
            conv_y = h

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

            h, w, ch = self.getImageShape(self.image_rescaled)

            mouse_x = event.pos().x() - self.offset[0]
            mouse_y = event.pos().y() - self.offset[1]

            if(mouse_x < 0): x = 0
            elif(mouse_x > w): x = w
            else: x = mouse_x/w
            
            if(mouse_y < 0): y = 0
            elif(mouse_y > h): y = h
            else: y = mouse_y/h
            
            self.start = [x, y]

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton & self.roi_enabled:
            h, w, ch = self.getImageShape(self.image_rescaled)

            mouse_x = event.pos().x() - self.offset[0]
            mouse_y = event.pos().y() - self.offset[1]

            if(mouse_x < 0): x = 0
            elif(mouse_x > w): x = w
            else: x = mouse_x/w
            
            if(mouse_y < 0): y = 0
            elif(mouse_y > h): y = h
            else: y = mouse_y/h

            self.end = [x, y]

            self.update()


    def setPixmap(self, pix):
        self.pix_map = pix
        self.update()

    def paintEvent(self, event):
        if not self.pix_map.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            # Check if there is an image
            if self.image is not None:
                self.resizeFrame()
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
        h, w, ch = self.getImageShape(self.image)

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

        # Apply roi if present
        if(self.start is not None and self.end is not None):
            start = [
                round(self.start[0]*nW), 
                round(self.start[1]*nH)
            ]

            end = [
                round(self.end[0]*nW), 
                round(self.end[1]*nH)
            ]

            resized_frame = cv2.rectangle(resized_frame, start, end, PORTARIT_ROI_COLOR, 2)

        # Generate final target size and fill with black color
        if(ch):
            f_frame = np.zeros((H, W, ch), np.uint8)
        else:
            f_frame = np.zeros((H, W), np.uint8)

        # Position resized frame inside final frame
        aH, aW = (H-nH)//2, (W-nW)//2
        self.offset = [aW, aH]
        f_frame[aH:aH+nH, aW:aW+nW] = resized_frame

        self.image_rescaled = resized_frame
        self.image_resized = f_frame