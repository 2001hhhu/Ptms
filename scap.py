from warnings import filterwarnings
from prometheus_client import Gauge
filterwarnings("ignore")
from scapy.all import *
import time
from collections import defaultdict
info = defaultdict(int)


def PackCallBack(packet):
    # packet是在网卡抓到的帧，每取一次payload就相当于向上解封装一次。
    # 打印源IP，源端口，目的IP，目的端口
    # if packet.haslayer('HTTP'):
    # http = packet.payload.payload.payload
    # print(http.show())
    # print("[%s]%s:%s-->%s:%s" % (packet['IP'].len, packet['IP'].src, packet.sport, packet['IP'].dst, packet.dport))
    # net_data.setdefault(packet['IP'].dst, 0)
    # net_data[packet['IP'].dst] += packet.len
    # # 打印数据包
    # print('-----------')
    # print(packet.show())
    # print('-----------')
    # print(net_data)
    global info
    if packet.haslayer('IP'):
        print(packet['IP'].sport, packet['IP'].len + 18)
        port = packet['IP'].sport
        length = packet['IP'].len + 18
        # if port in info:
        #     info[port] = info[port] + length
        # else:
        #     info = info | {port: length}
        info[port] = info[port] + length
    # print(packet)


if __name__ == '__main__':
    """
        count:抓取报的数量，设置为0时则一直捕获
        store:保存抓取的数据包或者丢弃，1保存，0丢弃
        offline:从pcap文件中读取数据包，而不进行嗅探，默认为None
        prn:为每个数据包定义一个回调函数，通常使用lambda表达式来写回调函数
        filter:过滤规则，可以在里面定义winreshark里面的过滤语法，使用 Berkeley Packet Filter (BPF)语法，具体参考：[http://blog.csdn.net/qwertyupoiuytr/article/details/54670477](http://blog.csdn.net/qwertyupoiuytr/article/details/54670477)
        L2socket:使用给定的L2socket
        timeout:在给定的事件后停止嗅探，默认为None
        opened_socket:对指定的对象使用.recv进行读取
        stop_filter:定义一个函数，决定在抓到指定的数据之后停止
        iface:指定抓包的网卡,不指定则代表所有网卡
    """

packets = sniff(count=0, prn=PackCallBack, iface='以太网', timeout=10)

print(info)
