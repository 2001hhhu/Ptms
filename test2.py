from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from network_state import Network
from scapy.all import *
import time
import optparse
import dpkt
import psutil
import pywin32


class te:

    def __init__(self):
        self.pids = psutil.pids()
        self.l = len(self.pids)



    def get_name(self):
        process_names = []
        for id in self.pids:
            process_name = psutil.Process(id).name()
            process_names.append(process_name)
            print(process_name)
        return process_names


    def getnet(self):
        process_nets_1 = []
        process_nets_2 = []
        return process_nets_1,process_nets_2


    def catch_pack(self):
        sniff(prn = self.printPacket, filter ="tcp")


    def printPacket(self,packet):
        print('src:%s----->dst:%s' % (packet[IP].src, packet[IP].dst))
        print('TTL:%s' % packet[IP].ttl)
        print(packet.show())
        # wrpcap('foo,cap',[packet])




if __name__ == '__main__':
    test = te()
    names = test.get_name()

    # te.catch_pack()
