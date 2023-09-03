from this import s

import psutil
import time
import socket


class Network:

    # bytes sent_1,sent_2,recv_1,recv_2,sent_rate,recv_rate;

    def __init__(self):
        self.a = 1




    def bytes2human(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return '%sB' % n


    def getdata(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        data = {
            'hostname':hostname,
            'ip':ip
        }
        return data

    def getmemory(self):
        mem = psutil.virtual_memory()
        zj = float(mem.total)/1024/1024/1024
        ysy = float(mem.used)/1024/1024/1024
        kx = float(mem.free)/1024/1024/1024
        return zj,ysy,kx

    def getcpu(self):
        cpu = (str(psutil.cpu_percent(1))) + '%'
        return cpu

    def getnet(self):
        sent_1 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_sent
        recv_1 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_recv
        time.sleep(1)
        sent_2 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_sent
        recv_2 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_recv
        sent_rate = (sent_2 - sent_1)/1024
        recv_rate = (recv_2 - recv_1)/1024
        return sent_rate,recv_rate



if __name__ == '__main__':
    net = Network()