def print_host(host, status):
    print(host["addr_type"], "host", host["addr"])
    print("Hostnames: ")
    for hostname in host["hostnames"]:
        print("    ", hostname)
    print("Ports: ")
    for port in host["ports"]:
        print("    ", port)
    print("OS: ")
    for oss in host["os_list"]:
        print("    ", oss)
    print("Fingerprint: ")
    for finger in host["fingers"]:
        print(finger)
    print("Status: ")
    if status["cnt"] < 10:
        print("    UNKNOWN", status["type"])
    else:
        print("    ", status["type"])


def get_ip_prefix(ip):
    tmp = ip.split(".")
    prefix = int(tmp[0]) * 65536 + int(tmp[1]) * 256 + int(tmp[2])
    return prefix


def prefix_to_ip(prefix):
    t1 = prefix % 256
    prefix -= t1
    prefix /= 256
    t2 = prefix % 256
    prefix -= t2
    prefix /= 256
    t3 = prefix
    return str(int(t3)) + "." + str(int(t2)) + "." + str(int(t1)) + ".0"
