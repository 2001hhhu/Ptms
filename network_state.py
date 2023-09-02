import psutil
import time
import socket


class Network:

    # bytes sent_1,sent_2,recv_1,recv_2,sent_rate,recv_rate;

    def __init__(self):
        self.sent_1 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_sent
        self.recv_1 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_recv

        time.sleep(1)

        self.sent_2 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_sent
        self.recv_2 = psutil.net_io_counters(pernic=True)['WLAN'].bytes_recv

        self.sent_rate = self.sent_2 - self.sent_1
        self.recv_rate = self.recv_2 - self.recv_1

        self.cpu_amount = psutil.cpu_count()
        self.cpu_percent = psutil.cpu_percent()

    def show(self):
        print(f"CPU的个数为{self.cpu_amount}")
        print(f"CPU的使用率为{self.cpu_percent}")


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

if __name__ == '__main__':
    net = Network()