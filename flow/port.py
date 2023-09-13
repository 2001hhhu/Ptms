from warnings import filterwarnings
filterwarnings("ignore")
from scapy.all import *
from collections import defaultdict
import socket
import processname

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
        process_name_to_port = processname.get_process_name()
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
                process_name_flow[item]["upload"] - temp_flow[item]["upload"]
            ) / (time_sum * 1024 * 1024)
            process_name_flow[item]["download_rate"] = (
                process_name_flow[item]["download"] - temp_flow[item]["download"]
            ) / (time_sum * 1024 * 1024)
            process_name_flow[item]["all_rate"] = (
                process_name_flow[item]["all"] - temp_flow[item]["all"]
            ) / (time_sum * 1024 * 1024)
        print(process_name_flow["BaiduNetdiskHost.exe"])


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class Packet:
    def __init__(self):

        self.IP = get_local_ip()
        self.info = defaultdict(lambda: {"upload": 0, "download": 0})

    def PackCallBack(self, packet):

        if packet.haslayer("IP"):
            currentIp = packet["IP"].src
            if self.IP == currentIp:

                port = packet["IP"].sport

                length = packet["IP"].len + 18
                self.info[port]["upload"] += length

            else:
                port = packet["IP"].dport
                length = packet["IP"].len + 18
                self.info[port]["download"] += length

    def get_packet(self):
        sniff(count=0, prn=self.PackCallBack)


if __name__ == "__main__":
    threads = []
    packet = Packet()
    t1 = threading.Thread(target=packet.get_packet)
    t2 = threading.Thread(target=get_flow)
    threads += [t1, t2]
    for t in threads:
        t.start()
