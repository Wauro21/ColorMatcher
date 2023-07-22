from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QMainWindow, QGroupBox, QLabel, QFormLayout, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
import sys
import os


class ResultWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects

        # Widgets

        self.process_results_btn = QPushButton('Procesar', self)
        self.result_group = QGroupBox('Resultados Análisis',self)
        self.distance_red = QLabel('-', self)
        self.distance_green = QLabel('-', self)
        self.distance_blue = QLabel('-', self)
        self.percentage_red = QLabel('-', self)
        self.percentage_green = QLabel('-', self)
        self.percentage_blue = QLabel('-', self)
        self.average_distance = QLabel('-', self)
        self.percentage_distance = QLabel('-', self)

        # init routines
        self.result_group.setStyleSheet(
            '''
            QGroupBox { font-weight: bold;}
            '''
        )


        # signals and slots

        # layout
        layout = QVBoxLayout()
        
        # fields layout
        fields = QHBoxLayout()

        field_layout_left = QFormLayout()
        field_layout_left.addRow('Distancia Rojo:', self.distance_red)
        field_layout_left.addRow('Distancia Verde:', self.distance_green)
        field_layout_left.addRow('Distancia Azul:', self.distance_blue)
        field_layout_left.addRow('Distancia Promedio:', self.average_distance)

        field_layout_right = QFormLayout()
        field_layout_right.addRow('Distancia Rojo %:', self.percentage_red)
        field_layout_right.addRow('Distancia Verde %:', self.percentage_green)
        field_layout_right.addRow('Distancia Azul %:', self.percentage_blue)
        field_layout_right.addRow('Distancia Promedio %:', self.percentage_distance)

        fields.addLayout(field_layout_left)
        fields.addLayout(field_layout_right)

        self.result_group.setLayout(fields)

        layout.addWidget(self.result_group)
        layout.addWidget(self.process_results_btn)
        
        self.setLayout(layout)

if __name__ == '__main__':

    app = QApplication([])
    if os.name == 'nt':
        app.setStyle('Fusion')
    window = ResultWidget()
    window.show()
    sys.exit(app.exec_())