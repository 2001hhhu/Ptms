import threading

from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QStringListModel, QTimer
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import random
import time
import numpy as np
from network_state import Network
from port import Pp

from chart import chart_1

plt.rcParams['font.sans-serif'] = ['SimHei']

class MplWidget2(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        # vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

class MplWidget3(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas_2 = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas_2)
        # vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas_2.axes = self.canvas_2.figure.add_subplot(112)
        self.setLayout(vertical_layout)


class Stats(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        designer_file = QFile("qt_2.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget2)
        self.ui = loader.load(designer_file, self)
        self.ui.setWindowTitle("端口流量监控系统")
        self.ui.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_4.setText(time.strftime('%Y年%m月%d日'))
        self._list = ["进程一"]
        self.showList()
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

        # self.ui.pushButton.clicked.connect(self.update_graph)
        self.ui.button1.clicked.connect(self.setGraph)
        self.ui.btg1.buttonClicked.connect(self.btnGroup1)
        self.ui.btg2.buttonClicked.connect(self.btnGroup2)
        self.ui.btg3.buttonClicked.connect(self.btnGroup3)
        self.ui.Timer_1 = QTimer()
        self.ui.Timer_2 = QTimer()
        self.ui.Timer_3 = QTimer()
        self.ui.Timer_4 = QTimer()
        self.ui.Timer_5 = QTimer()
        self.lcd_styleRule()
        self.m = [0.0]
        self.n = [0.0]
        self.t = [0.0]
        self.t_now = 0.0
        self.x = [0.0]
        self.k = [0.0]
        self.t_now_2 = 0.0
        self.t_2 = [0.0]
        self.st = ""

        # self.setTextBrowser_1()
        # self.setTextBrowser_2()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

    def update_graph(self):
        # matplotlib中文问题
        self.t_now = self.t_now + 1.0
        self.t.append(self.t_now)
        net = Network()
        sent_rate, recv_rate = net.getnet()
        # if sent_rate > 1024.0 and recv_rate > 1024.0:
        #     # MB/s
        #     sent_rate = sent_rate / 1024
        #     recv_rate = recv_rate / 1024
        # else:
        #     # KB/s
        #     print(1)

        self.m.append(recv_rate)
        self.n.append(sent_rate)

        self.ui.asss.canvas.axes.clear()
        self.ui.asss.canvas.axes.set_xlabel(xlabel="时间(s)")
        self.ui.asss.canvas.axes.set_ylabel(ylabel="下载速度(KB/s)/上传速度(KB/s)")
        self.ui.asss.canvas.axes.plot(self.t, self.m, color="yellow", label="下载速度")
        self.ui.asss.canvas.axes.plot(self.t, self.n, color="red", label="上传速度")
        self.ui.asss.canvas.axes.legend()
        self.ui.asss.canvas.axes.set_title('总流量图')
        self.ui.asss.canvas.draw()

    def update_graph_2(self):
        self.t_now_2 = self.t_now_2 + 1.0
        self.t_2.append(self.t_now_2)
        net = Network()
        sent_rate, recv_rate = net.getnet()
        self.x.append(recv_rate)
        self.k.append(sent_rate)
        st = self.st

        self.ui.widget.canvas.axes.clear()
        self.ui.widget.canvas.axes.set_xlabel(xlabel="时间(s)")
        self.ui.widget.canvas.axes.set_ylabel(ylabel="下载速度(KB/s)/上传速度(KB/s)")
        self.ui.widget.canvas.axes.plot(self.t, self.m, color="yellow", label="下载速度")
        self.ui.widget.canvas.axes.plot(self.t, self.n, color="red", label="上传速度")
        self.ui.widget.canvas.axes.legend()
        self.ui.widget.canvas.axes.set_title(f"{st}流量图")
        self.ui.widget.canvas.draw()

    def setGraph(self):
        self.ui.Timer_4.start()
        self.ui.Timer_4.timeout.connect(self.update_graph)
        self.ui.Timer_4.setInterval(1000)

    def setTextBrowser_1(self):
        net = Network()
        sent_rate, recv_rate = net.getnet()
        if sent_rate > 1024.0 and recv_rate > 1024.0:
            sent_rate = sent_rate / 1024
            recv_rate = recv_rate / 1024
            self.ui.textBrowser_1.setPlainText("上传：{0}MB/s".format("%.2f" % sent_rate))
            self.ui.textBrowser_1.append("下载：{0}MB/s".format("%.2f" % recv_rate))
        else:
            self.ui.textBrowser_1.setPlainText("上传：{0}KB/s".format("%.2f" % sent_rate))
            self.ui.textBrowser_1.append("下载：{0}KB/s".format("%.2f" % recv_rate))
            # time.sleep(1)

    def setTextBrowser_3(self):
        net = Network()
        devices, ison = net.getNetStats()
        for i in range(len(devices)):
            if ison[i] and i == 0:
                self.ui.textBrowser_3.setPlainText("网卡：" + devices[i] + "已启动")
            elif ison[i] and i != 0:
                self.ui.textBrowser_3.append("网卡：" + devices[i] + "已启动")
            elif ison[i] and i == 0:
                self.ui.textBrowser_3.setPlainText("网卡：" + devices[i] + "未启动")
            else:
                self.ui.textBrowser_3.append("网卡：" + devices[i] + "未启动")

    def setTextBrowser_6(self):
        net = Network()
        data = net.getdata()
        cpu = net.getcpu()
        zj, ysy, kx = net.getmemory()
        self.ui.textBrowser_6.setPlainText("电脑主机：" + data['hostname'])
        self.ui.textBrowser_6.append("IP地址：" + data['ip'])
        self.ui.textBrowser_6.append("cpu的利用率：%s" % cpu)
        self.ui.textBrowser_6.append("系统总计内存：%d.4GB" % zj)
        self.ui.textBrowser_6.append("系统已使用内存：%d.4GB" % ysy)
        self.ui.textBrowser_6.append("系统空闲内存：%d.4GB" % kx)

    def btnGroup1(self):
        itemID = self.ui.btg1.checkedButton()
        itemText = self.ui.btg1.checkedButton().text()
        print(itemText)
        if itemText == "图形概览":
            self.ui.stack_1.setCurrentIndex(3)
        elif itemText == "网络流量":
            self.ui.stack_1.setCurrentIndex(0)
            self.ui.Timer_1.start()
            self.ui.Timer_1.timeout.connect(self.setTextBrowser_1)
            self.ui.Timer_1.setInterval(1000)
        elif itemText == "网络设备":
            self.ui.stack_1.setCurrentIndex(1)
            self.ui.Timer_2.start()
            self.ui.Timer_2.timeout.connect(self.setTextBrowser_6)
            self.ui.Timer_2.timeout.connect(self.setTextBrowser_3)
            self.ui.Timer_2.setInterval(1000)
        elif itemText == "提醒":
            self.ui.stack_1.setCurrentIndex(2)
        if itemText != "网络流量":
            self.ui.Timer_1.stop()
        if itemText != "网络设备":
            self.ui.Timer_2.stop()
        # if itemText != "提醒":
        #     self.ui.Timer_3.stop()

    def btnGroup2(self):
        itemText = self.ui.btg2.checkedButton().text()
        print(itemText)
        if itemText == "全部":
            self.ui.stack_2.setCurrentIndex(0)
        elif itemText == "应用程序":
            self.ui.stack_2.setCurrentIndex(1)

    def btnGroup3(self):
        itemText = self.ui.btg3.checkedButton().text()
        print(itemText)
        if itemText == "全部":
            self.ui.stack_3.setCurrentIndex(0)
        elif itemText == "未读":
            self.ui.stack_3.setCurrentIndex(1)

    def showList(self):
        # 进程列表的获取与事件
        model = QStringListModel()
        model.setStringList(self._list)
        self.ui.listView.setModel(model)
        self.ui.listView.clicked.connect(self.getProcess)

    def getProcess(self, item):
        print(self._list[item.row()])
        if self._list[item.row()] == "进程一":
            self.st = "进程一"
            self.ui.Timer_5.start()
            self.ui.Timer_5.timeout.connect(self.update_graph_2)


    def lcd_styleRule(self):
        self.ui.LCD.setSegmentStyle(QLCDNumber.Flat)
        self.ui.LCD.setDigitCount(19)
        self.ui.Timer_3.timeout.connect(self.showTime)
        self.ui.Timer_3.start()
        self.ui.Timer_3.setInterval(1000)

    def showTime(self):
        # 格式化时间显示
        BJ_time = time.strftime('%Y-%m-%d %H:%M:%S')
        # 槽函数 display():显示字符串数值
        self.ui.LCD.display(BJ_time)

    # def getlist(self):
    #     port = Pp()
    #     p_info = Pp.info
    #     p_list = []
    #     port.run()
    #     for key,values in p_info.items():
    #         str = "" + key + "↓:" + self.hum_convert(values[0]) + "↑:" + self.hum_convert(values[1])
    #         print(str)
    #         p_list.append(str)

    def hum_convert(self, value):
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for i in range(len(units)):
            if (value / size) < 1:
                return "%.2f%s" % (value, units[i])
            value = value / size


if __name__ == '__main__':
    # p = Pp()
    # threads = []
    # t1 = threading.Thread(target=p.get_packet)
    # threads.append(t1)
    # t1.start()
    app = QApplication([])
    window = Stats()
    window.show()
    app.exec()
