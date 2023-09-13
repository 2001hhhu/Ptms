from scapy.all import *
import psutil
from pprint import pprint

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

# pprint(port_name)
'''port to name is done'''

name_port = {}

for key, value in port_name.items():
    # print('key: ', key, 'value: ', value)
    name_port.setdefault(value, []).append(key)

# pprint(name_port)

for i in range(len(name_port['msedge.exe'])):
    print(name_port['msedge.exe'][i])
