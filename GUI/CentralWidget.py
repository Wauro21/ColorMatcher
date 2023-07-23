from GUI.Constants import PROCESS_IMAGE_TITLE, REFERENCE_IMAGE_TITLE
from GUI.ImageHolder import ImageViewer
from GUI.MessageBox import ErrorBox
from GUI.ResultWidget import ResultWidget
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide2.QtCore import Signal, Slot, Qt
import numpy as np

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects


        # Widgets
        self.reference_image = ImageViewer(
                                            REFERENCE_IMAGE_TITLE,
                                            self
                                            )

        self.process_image = ImageViewer(
                                            PROCESS_IMAGE_TITLE,
                                            self
                                        )
        
        self.result_widget = ResultWidget(self)

        # init routines

        # signals and slots
        self.result_widget.ask_process.connect(self.processResults)

        # layout
        layout = QHBoxLayout()

        # Frames layout
        layout.addWidget(self.reference_image)
        layout.addWidget(self.process_image)

        # Result layout
        result = QVBoxLayout()
        result.addWidget(self.result_widget)
        result.addStretch(1)


        layout.addLayout(result)
        
        self.setLayout(layout)

    def processResults(self):

        # Check if ready
        reference_flag = self.reference_image.roiReady()
        process_flag = self.process_image.roiReady()

        if not(reference_flag and process_flag):
            message = ErrorBox('¡No se han seleccionado las regiones de interés de las imágenes a comparar!')
            message.exec_()
            return

        # Get color from frames
        reference_color = self.reference_image.getColor()
        evaluated_color = self.process_image.getColor()

        # Get color distances
        max_pixel_value = 255
        channel_diffs = []
        channel_diffs_percentages = []

        for i in range(3):
            temp = abs(reference_color[i] - evaluated_color[i])
            channel_diffs.append(temp)
            channel_diffs_percentages.append(100*temp/max_pixel_value)

        # Get average metrics 
        average_distance = np.average(channel_diffs)
        average_distance_percentage = 100*average_distance/255

        self.result_widget.updateValues(
            channel_diffs, 
            channel_diffs_percentages, 
            average_distance, 
            average_distance_percentage
        )
        
