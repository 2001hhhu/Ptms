from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from network_state import Network

class Stats:

    def __init__(self):
        path = 'qt_2.ui'
        self.ui = QUiLoader().load(path)
        self.setTextBrowser()



    def setTextBrowser(self):
        net = Network()
        data = net.getdata()
        self.ui.textBrowser.setPlainText("电脑主机：" + data['hostname'])
        self.ui.textBrowser.append("IP地址：" + data['ip'])
