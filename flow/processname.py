
import os
import time

import subprocess

def run_cmd(cmd):
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    output = result.stdout.splitlines()
    return output

process_name_to_port = {}
def get_process_name():
    cmd = "netstat -nbo"
    data = run_cmd(cmd)
    rows = []
    for i, line in enumerate(data):
        if i == 0:
            header = line.split()
            rows.append(header)
        else:
            row = line.split()
            rows.append(row)
    del rows[0:4]
    inf = {}
    for i, item in enumerate(rows):
        if len(item) == 5 and item[4] != "0":
            process_name = rows[i + 1][0].replace("[", "")
            process_name = process_name.replace("]", "")
            inf[int(item[1].split(":")[-1])] = process_name


    # process_name_to_port = {}
    for item in inf:
        if inf[item] not in process_name_to_port:
            process_name_to_port[inf[item]] = [item]
        else:
            if item not in process_name_to_port[inf[item]]:
              process_name_to_port[inf[item]] += [item]

    return process_name_to_port




