from scapy.all import *
import psutil
from pprint import pprint
count = 0


def traffic_monitor_callbak(pkt):
    global count
    if pkt.haslayer('IP'):
        count += pkt['IP'].len + 18


def test(pkt):
    print(pkt.show())


def docount():
    global count
    sniff(prn=traffic_monitor_callbak, store=0, timeout=1)
    print(count)
    count = 0

# if __name__ == '__main__':
#     while True:
#         docount()


# sniff(filter='port 1630', prn=lambda x:x.summary(), timeout=10)
# print(pkt.sprintf("%IP.len%"))

port_name = {}


def netpidport(name, pid):
    """根据pid寻找该进程对应的端口"""
    # 获取当前的网络连接信息
    net_con = psutil.net_connections()
    for con_info in net_con:
        if con_info.pid == pid:
            port_name[con_info.laddr.port] = name


for proc in psutil.process_iter():
    try:
        processName = proc.name()
        processID = proc.pid
        netpidport(processName, processID)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

pprint(port_name)