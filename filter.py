import os
import json
import argparse
from utils import *

IP_TAIL_RATE = 0.1
IP_STAT_THRES = 0.8
IP_DEAD_THRES = 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, help="input type")
    parser.add_argument("--input", type=str, help="input dir")
    parser.add_argument("--output", type=str, help="output file")
    args = parser.parse_args()
    print(args)
    

    prefix_cnt = {}
    res_cnt = 0

    if args.type == "os":
        iptable = {}
        file_list = os.listdir(args.input)
        for filename in file_list:
            with open(args.input + "/" + filename, "r") as f:
                hosts = json.load(f)
            for host in hosts:
                if host["addr"] not in iptable:
                    iptable[host["addr"]] = []
                iptable[host["addr"]].append(host)
            res_cnt += 1

        for ip in iptable:
            prefix = get_ip_prefix(ip)
            if prefix not in prefix_cnt:
                prefix_cnt[prefix] = [0 for _ in range(res_cnt + 1)]
            prefix_cnt[prefix][len(iptable[ip])] += 1

    if args.type == "ip":
        iptable = {}
        file_list = os.listdir(args.input)
        for filename in file_list:
            with open(args.input + "/" + filename, "r") as f:
                lines = f.readlines()
            for line in lines:
                ip = line.strip()
                if ip == "":
                    continue
                if line.strip() not in iptable:
                    iptable[ip] = 0
                iptable[ip] += 1
            res_cnt += 1

        for ip in iptable:
            prefix = get_ip_prefix(ip)
            if prefix not in prefix_cnt:
                prefix_cnt[prefix] = [0 for _ in range(res_cnt + 1)]
            prefix_cnt[prefix][iptable[ip]] += 1


    tail_num = int(res_cnt * IP_TAIL_RATE) + 1
    sorted_cnt = sorted(prefix_cnt.items(), key=lambda d:d[0])
    result = []
    for prefix, cnt_list in sorted_cnt:
        tail_cnt = sum(cnt_list[-tail_num:])
        total_cnt = sum(cnt_list)
        tmp = {"ip": prefix_to_ip(prefix), "tail_cnt": tail_cnt, "cnt": total_cnt}
        if tail_cnt / total_cnt < 0.8:
            tmp["type"] = "dynamic"
        else:
            tmp["type"] = "static"
        result.append(tmp)

    with open(args.output, "w") as f:
        json.dump(result, f)
