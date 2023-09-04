from scapy.all import *

count = 0


def traffic_monitor_callbak(pkt):
    global count
    if IP in pkt:
        count += pkt[IP].len


def docount():
    global count
    sniff(prn=traffic_monitor_callbak, store=0, timeout=1)
    print(count)
    count = 0


while True:
    docount()



# sniff(filter='port 1630', prn=lambda x:x.summary(), timeout=10)
# print(pkt.sprintf("%IP.len%"))