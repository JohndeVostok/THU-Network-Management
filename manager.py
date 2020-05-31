import json
from utils import *

FP_DATA = "res_fp.json"
IP_DATA = "res_ip.json"

if __name__ == "__main__":
    with open(FP_DATA, "r") as f:
        hosts = json.load(f)
    ip_table = {}
    for host in hosts:
        ip_table[host["addr"]] = host
    with open(IP_DATA, "r") as f:
        ips = json.load(f)
    prefix_table = {}
    for ip_meta in ips:
        prefix = get_ip_prefix(ip_meta["ip"])
        prefix_table[prefix] = ip_meta

    while True:
        ip = input("ip: ")
        if ip == "exit":
            break
        prefix = get_ip_prefix(ip)
        if ip not in ip_table or prefix not in prefix_table:
            print("IP not detected.")
            continue
        host = ip_table[ip]
        status = prefix_table[prefix]
        print_host(host, status)

