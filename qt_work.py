from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader


class Stats:

    def __init__(self):
        self.path = 'D:\\QtUi\\qt_1.ui'
        self.ui = QUiLoader().load(self.path)
