from warnings import filterwarnings
filterwarnings("ignore")
from matplotlib.figure import Figure
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QStringListModel, QTimer
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from network_state import Network
from flow.port import *


process_name_flow = defaultdict(
    lambda: {
        "upload": 0,
        "download": 0,
        "all": 0,
        "upload_rate": 0.0000,
        "download_rate": 0.0000,
        "all_rate": 0.0000,
    }
)


def get_flow():
    while True:
        process_name_to_port = get_process_name()
        # print(process_name_to_port)
        temp_flow = copy.deepcopy(process_name_flow)
        process_name_flow.clear()

        for item in process_name_to_port:
            for port in process_name_to_port[item]:
                process_name_flow[item]["upload"] += packet.info[port]["upload"]
                process_name_flow[item]["download"] += packet.info[port]["download"]
                process_name_flow[item]["all"] = (
                        process_name_flow[item]["download"]
                        + process_name_flow[item]["upload"]
                )

        time.sleep(3)

        time_sum = 3.0
        for item in process_name_flow:
            process_name_flow[item]["upload_rate"] = (
                                                             process_name_flow[item]["upload"] - temp_flow[item][
                                                         "upload"]
                                                     ) / (time_sum * 1024 * 1024)
            process_name_flow[item]["download_rate"] = (
                                                               process_name_flow[item]["download"] - temp_flow[item][
                                                           "download"]
                                                       ) / (time_sum * 1024 * 1024)
            process_name_flow[item]["all_rate"] = (
                                                          process_name_flow[item]["all"] - temp_flow[item]["all"]
                                                  ) / (time_sum * 1024 * 1024)
        # print(process_name_flow)


plt.rcParams['font.sans-serif'] = ['SimHei']


class MplWidget2(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


class FigureCanvasDemo2(FigureCanvas):
    def __init__(self, parent=None, width=10, height=5):
        # 创建一个Figure 如果不加figsize 显示图像过大 需要缩小
        fig = plt.Figure(figsize=(width, height), tight_layout=True)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)


class Stats(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        designer_file = QFile("qt_2.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget2)
        self.ui = loader.load(designer_file, self)
        self.ui.setWindowTitle("端口流量监控系统")
        self.graphicsScene = QGraphicsScene()
        self.ui.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_4.setText(time.strftime('%Y年%m月%d日'))
        self.p_list = []
        self._list = []
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
        self.ui.Timer_6 = QTimer()
        self.ui.Timer_7 = QTimer()
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
        self.visual_data = FigureCanvasDemo2(width=self.ui.graphicsView.width() / 101,
                                             height=self.ui.graphicsView.height() / 101)


        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)

    def update_graph(self):
        # matplotlib中文问题
        self.t_now = self.t_now + 1.0
        self.t.append(self.t_now)
        net = Network()
        sent_rate, recv_rate = net.getnet()

        self.m.append(recv_rate)
        self.n.append(sent_rate)

        self.ui.asss.canvas.axes.clear()
        self.ui.asss.canvas.axes.set_xlabel(xlabel="时间(s)")
        self.ui.asss.canvas.axes.set_ylabel(ylabel="下载速度(KB/s)/上传速度(KB/s)")
        self.ui.asss.canvas.axes.plot(self.t, self.m, color="yellow", label="下载速度")
        self.ui.asss.canvas.axes.plot(self.t, self.n, color="red", label="上传速度")
        self.ui.asss.canvas.axes.legend()
        self.ui.asss.canvas.axes.set_title('总网速图')
        self.ui.asss.canvas.draw()

    def update_graph_2(self):
        self.t_now_2 = self.t_now_2 + 1.0
        self.t_2.append(self.t_now_2)
        str_1 = ""
        str_2 = ""
        for key, values in process_name_flow.items():
            if key == self.st:
                str_1 = values['download']
                str_2 = values['upload']


        self.x.append(str_1)
        self.k.append(str_2)
        st = self.st


        self.visual_data.axes.clear()
        self.visual_data.axes.set_xlabel(xlabel="时间(s)")
        self.visual_data.axes.set_ylabel(ylabel=f"下载流量(B)/上传流量(B)")
        self.visual_data.axes.plot(self.t_2, self.x, color="yellow", label="下载流量")
        self.visual_data.axes.plot(self.t_2, self.k, color="red", label="上传流量")
        self.visual_data.axes.grid()
        self.visual_data.axes.legend()
        self.graphicsScene.addWidget(self.visual_data)
        self.ui.graphicsView.setScene(self.graphicsScene)
        self.ui.graphicsView.show()
        self.visual_data.draw()

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

    def setTextBrowser_2(self):
        list_1 = self.getNet()
        self.ui.textBrowser_2.setPlainText("各应用程序流量：")
        for st in list_1:
            self.ui.textBrowser_2.append(st)

    def setTextBrowser_3(self):
        net = Network()
        devices, ison = net.getNetStats()
        strs = []
        for i in range(len(devices)):
            if ison[i] and i == 0:
                strs.append("网卡：" + devices[i] + "已启动")
            elif ison[i] and i != 0:
                strs.append("网卡：" + devices[i] + "已启动")
            elif ison[i] and i == 0:
                strs.append("网卡：" + devices[i] + "未启动")
            else:
                strs.append("网卡：" + devices[i] + "未启动")
        self.ui.textBrowser_3.setPlainText(strs[0])
        self.ui.textBrowser_3.append(strs[1])
        self.ui.textBrowser_3.append(strs[2])
        self.ui.textBrowser_3.append(strs[3])
        self.ui.textBrowser_3.append(strs[4])

    def setTextBrowser_5(self):
        self.ui.textBrowser_5.setPlainText("未读信息：")
        for key, values in process_name_flow.items():
            str_1 = self.hum_convert(values['all'])
            ch = f"{str_1[-2]}{str_1[-1]}"
            if ch == "GB":
                self.ui.textBrowser_5.append(f"应用{key}已用{str_1}流量")

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
            self.ui.Timer_7.start()
            self.ui.Timer_7.timeout.connect(self.setTextBrowser_2)
            self.ui.Timer_7.setInterval(1000)
        elif itemText == "网络设备":
            self.ui.stack_1.setCurrentIndex(1)
            self.ui.Timer_2.start()
            self.ui.Timer_2.timeout.connect(self.setTextBrowser_6)
            self.setTextBrowser_3()
            # self.ui.Timer_2.timeout.connect(self.setTextBrowser_3)
            self.ui.Timer_2.setInterval(1000)
        elif itemText == "提醒":
            self.ui.stack_1.setCurrentIndex(2)
        if itemText != "网络流量":
            self.ui.Timer_1.stop()
            self.ui.Timer_7.stop()
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
            self.ui.Timer_6.start()
            self.ui.Timer_6.timeout.connect(self.showList)
            self.ui.Timer_6.setInterval(1000)
        elif itemText != "应用程序":
            self.ui.Timer_6.stop()

    def btnGroup3(self):
        itemText = self.ui.btg3.checkedButton().text()
        print(itemText)
        if itemText == "全部":
            self.ui.stack_3.setCurrentIndex(0)
        elif itemText == "未读":
            self.ui.stack_3.setCurrentIndex(1)
            self.setTextBrowser_5()

    def showList(self):
        # 进程列表的获取与事件
        self.getlist()
        model = QStringListModel()
        model.setStringList(self._list)
        self.ui.listView.setModel(model)
        self.ui.listView.clicked.connect(self.getProcess)

    def getProcess(self, item):
        # print(self._list[item.row()])
        self.st = ""
        for ch in self._list[item.row()]:
            # print(ch)
            if ch != " ":
                self.st = self.st + ch
            else:
                break
        print(self.st)
        self.ui.Timer_5.start()
        self.ui.Timer_5.timeout.connect(self.update_graph_2)
        self.ui.Timer_5.setInterval(1000)

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

    def getlist(self):
        self.p_list = []
        for key, values in process_name_flow.items():
            str_1 = self.hum_convert(values['download'])
            str_2 = self.hum_convert(values['upload'])
            _str = f"{key} 下载流量:{str_1} 上传流量:{str_2}"
            # print(_str)
            self.p_list.append(_str)
        self._list = self.p_list

    def getNet(self):
        list_1 = []
        for key, values in process_name_flow.items():
            str_1 = self.hum_convert(values['download'])
            str_2 = self.hum_convert(values['upload'])
            _str = f"{key} 下载流量:{str_1} 上传流量:{str_2}"
            # print(_str)
            list_1.append(_str)
        return list_1

    def hum_convert(self, value):
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for i in range(len(units)):
            if (value / size) < 1:
                return "%.2f%s" % (value, units[i])
            value = value / size


if __name__ == '__main__':
    threads = []
    packet = Packet()
    t1 = threading.Thread(target=packet.get_packet)
    t2 = threading.Thread(target=get_flow)
    threads += [t1, t2]
    for t in threads:
        t.start()
    app = QApplication([])
    window = Stats()
    window.show()
    app.exec()
