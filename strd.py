# import psutil
#
# def get_network_usage():
#     network_stats = psutil.net_io_counters()
#     return network_stats.bytes_sent, network_stats.bytes_recv
#
# bytes_sent, bytes_recv = get_network_usage()
# print(f"Bytes Sent: {bytes_sent/1024/1024}MB")
# print(f"Bytes Received: {bytes_recv}")
# Inserted code

import psutil
import time
def get_network_usage():
    network_stats = psutil.net_io_counters()
    return network_stats.bytes_sent, network_stats.bytes_recv

def monitor_network_traffic():
    while True:
        sent_before, received_before = get_network_usage()
        time.sleep(1)
        sent_after, received_after = get_network_usage()
        sent_speed = sent_after - sent_before
        received_speed = received_after - received_before
        print(f"Sent: {sent_speed} bytes/s, Received: {received_speed} bytes/s")

monitor_network_traffic()
