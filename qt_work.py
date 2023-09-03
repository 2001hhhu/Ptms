from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from network_state import Network


class Stats:

    def __init__(self):
        path = 'qt_2.ui'
        self.ui = QUiLoader().load(path)
        self.setTextBrowser_1()
        self.setTextBrowser_2()
        # self.ui.button2.clicked.connect(self.setTextBrowser_2)
        # self.net = Network()

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
