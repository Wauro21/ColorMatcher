from GUI.ImageHolder import ImageViewer
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
                                            'Imagen Referencia:',
                                            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                                            self
                                            )

        self.process_image = ImageViewer(
                                            'Imagen a procesar:',
                                            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                                            self
                                        )
        
        self.result_widget = ResultWidget(self)

        # init routines

        # signals and slots

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