from PySide2.QtWidgets import QMessageBox


__version__ ='0.1'
__author__ = 'maurio.aravena@sansano.usm.cl'



class ErrorBox(QMessageBox):
    
    def __init__(self, error_e, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Critical)
        self.setText('<b>An error has ocurred!</b>')
        self.setInformativeText(str(error_e))
        self.setWindowTitle('Error!')


class WarningBox(QMessageBox):
    def __init__(self, warning, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Warning)
        self.setText('<b>Warning:</b>')
        self.setInformativeText(warning)
        self.setWindowTitle('Warning!')

class InformationBox(QMessageBox):
    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setText('<b>Information:</b>')
        self.setInformativeText(info)
        self.setWindowTitle('Information!')

