from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from network_state import Network

class Stats:

    def __init__(self):
        self.path = 'D:\\QtUi\\qt_1.ui'
        self.ui = QUiLoader().load(self.path)
        self.setTextBrowser()



    def setTextBrowser(self):
        net = Network()
        self.ui.textBrowser.setPlainText(net.getdata())
