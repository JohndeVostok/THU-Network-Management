import os
import argparse
import json
from utils import print_host
from xml.dom import minidom

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="input dir")
    parser.add_argument("--output", type=str, help="output file")
    args = parser.parse_args()
    print(args)
    hosts = []

    file_list = os.listdir(args.input)
    for filename in file_list:
        if filename.split(".")[-1] != "xml":
            continue
        domTree = minidom.parse(args.input + "/" + filename)
        rootNode = domTree.documentElement
        hosts_node = rootNode.getElementsByTagName("host")
        for host_node in hosts_node:
            # Host
            host = {"addr": "", "addr_type": "", "hostnames": [], "ports": [], "os_list": []}

            # Address
            addr_node = host_node.getElementsByTagName("address")[0]
            addr = addr_node.getAttribute("addr")
            addr_type = addr_node.getAttribute("addrtype")
            host["addr"] = addr
            host["addr_type"] = addr_type
            
            # Hostnames
            hostnames_node = host_node.getElementsByTagName("hostnames")[0].getElementsByTagName("hostname")
            hostnames = []
            for hostname_node in hostnames_node:
                hostnames.append({"name": hostname_node.getAttribute("name"), "type": hostname_node.getAttribute("type")})
            host["hostnames"] = hostnames


            # Ports
            ports_node_root = host_node.getElementsByTagName("ports")
            if len(ports_node_root) > 0:
                ports_node = ports_node_root[0].getElementsByTagName("port")
                ports = []
                for port_node in ports_node:
                    port = {}
                    port["protocol"] = port_node.getAttribute("protocol")
                    port["portid"] = port_node.getAttribute("portid")
                    port["state"] = port_node.getElementsByTagName("state")[0].getAttribute("state")
                    port["service"] = port_node.getElementsByTagName("service")[0].getAttribute("name")
                    ports.append(port)
                host["ports"] = ports
        
            # OS
            os_root = host_node.getElementsByTagName("os")
            if len(os_root) > 0:
                os_list_node = os_root[0].getElementsByTagName("osmatch")
                os_list = []
                for os_node in os_list_node:
                    os = {}
                    os["name"] = os_node.getAttribute("name")
                    os["type"] = os_node.getElementsByTagName("osclass")[0].getAttribute("type")
                    os["vendor"] = os_node.getElementsByTagName("osclass")[0].getAttribute("vendor")
                    os["family"] = os_node.getElementsByTagName("osclass")[0].getAttribute("osfamily")
                    cpes_node = os_node.getElementsByTagName("osclass")[0].getElementsByTagName("cpe")
                    cpe = []
                    for cpe_node in cpes_node:
                        cpe.append(cpe_node.childNodes[0].data)
                    os["cpe"] = cpe
                    os_list.append(os)
                host["os_list"] = os_list
                fingers_node = os_root[0].getElementsByTagName("osfingerprint")
                fingers = []
                for finger_node in fingers_node:
                    finger = finger_node.getAttribute("fingerprint")
                    fingers.append(finger)
                host["fingers"] = fingers

            hosts.append(host)

    with open(args.output, "w") as f:
        json.dump(hosts, f)