from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import random
import numpy as np
from network_state import Network
from chart import chart_1


class MplWidget2(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        # vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


class Stats(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        designer_file = QFile("qt_2.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget2)
        self.ui = loader.load(designer_file, self)
        self.ui.btg1 = QButtonGroup()
        self.ui.btg2 = QButtonGroup()
        self.ui.btg3 = QButtonGroup()
        self.ui.btg1.addButton(self.ui.rbtn1, 1)
        self.ui.btg1.addButton(self.ui.rbtn2, 2)
        self.ui.btg1.addButton(self.ui.rbtn3, 3)
        self.ui.btg1.addButton(self.ui.rbtn4, 4)
        self.ui.btg2.addButton(self.ui.rbtn5, 5)
        self.ui.btg2.addButton(self.ui.rbtn6, 6)
        self.ui.btg3.addButton(self.ui.rbtn7, 7)
        self.ui.btg3.addButton(self.ui.rbtn8, 8)


        designer_file.close()

        #self.ui.pushButton.clicked.connect(self.update_graph)
        self.ui.button1.clicked.connect(self.update_graph)
        self.ui.btg1.buttonClicked.connect(self.btnGroup1)
        self.setTextBrowser_1()
        self.setTextBrowser_2()


        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.ui.asss.canvas.axes.clear()
        self.ui.asss.canvas.axes.plot(t, cosinus_signal)
        self.ui.asss.canvas.axes.plot(t, sinus_signal)
        self.ui.asss.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.ui.asss.canvas.axes.set_title('Cosinus - Sinus Signals')
        self.ui.asss.canvas.draw()

    def setTextBrowser_1(self):
        net = Network()
        data = net.getdata()
        cpu = net.getcpu()
        zj, ysy, kx = net.getmemory()
        self.ui.textBrowser.setPlainText("电脑主机：" + data['hostname'])
        self.ui.textBrowser.append("IP地址：" + data['ip'])
        self.ui.textBrowser.append("cpu的利用率：%s" % cpu)
        self.ui.textBrowser.append("系统总计内存：%d.4GB" % zj)
        self.ui.textBrowser.append("系统已使用内存：%d.4GB" % ysy)
        self.ui.textBrowser.append("系统空闲内存：%d.4GB" % kx)

    def setTextBrowser_2(self):
        net = Network()
        sent_rate, recv_rate = net.getnet()
        # while(1):
        #     if sent_rate > 1024.0 and recv_rate > 1024.0:
        #         sent_rate = sent_rate/1024
        #         recv_rate = recv_rate/1024
        #         self.ui.textBrowser_2.setPlainText("上传：{0}MB/s".format("%.2f"%sent_rate))
        #         self.ui.textBrowser_2.append("下载：{0}MB/s".format("%.2f"%recv_rate))
        #     else:
        #         self.ui.textBrowser_2.setPlainText("上传：{0}KB/s".format("%.2f"%sent_rate))
        #         self.ui.textBrowser_2.append("下载：{0}KB/s".format("%.2f"%recv_rate))
        if sent_rate > 1024.0 and recv_rate > 1024.0:
            sent_rate = sent_rate / 1024
            recv_rate = recv_rate / 1024
            self.ui.textBrowser_2.setPlainText("上传：{0}MB/s".format("%.2f" % sent_rate))
            self.ui.textBrowser_2.append("下载：{0}MB/s".format("%.2f" % recv_rate))
        else:
            self.ui.textBrowser_2.setPlainText("上传：{0}KB/s".format("%.2f" % sent_rate))
            self.ui.textBrowser_2.append("下载：{0}KB/s".format("%.2f" % recv_rate))


    def btnGroup1(self):
        itemID = self.ui.btg1.checkedButton()
        itemText = self.ui.btg1.checkedButton().text()
        print(itemID)
        print(itemText)
        if itemText == "图形概览":
            self.ui.stack_1.setCurrentIndex(3)
        elif itemText == "网络流量":
            self.ui.stack_1.setCurrentIndex(0)
        elif itemText == "网络设备":
            self.ui.stack_1.setCurrentIndex(1)
        elif itemText == "提醒":
            self.ui.stack_1.setCurrentIndex(2)





if __name__ == '__main__':
    app = QApplication([])
    window = Stats()
    window.show()
    app.exec()
