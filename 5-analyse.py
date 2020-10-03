#!/usr/bin/env python3
import sys
import subprocess
import logging
import json
from dataclasses import dataclass

from graph_tools import Graph

svc_dict = {}
pod_dict = {}
g = Graph()


def process_file(file):
    with open(file, "r") as a_file:
        capture_metadata = json.loads(a_file.read())
        build_service_map(capture_metadata["services"]["items"])
        build_pod_map(capture_metadata["pods"]["items"])
        for pod_metadata in capture_metadata["pod_metadata"]:
            handle_capture_per_pod(pod_metadata["pod"], file[: file.rindex('/')] + '/' + pod_metadata["file"],
                                   pod_metadata["IP"])
    analyze_graph()
    create_network_policy()

def build_service_map(service_items):
    for svc in service_items:
        svc_dict[svc["spec"]["clusterIP"]] = svc


def build_pod_map(pod_items):
    for pod in pod_items:
        pod_dict[pod["metadata"]["name"]] = pod


def handle_capture_per_pod(pod_name, capture_file_path, pod_ip):
    logging.debug('Pod: {}, Capture: {}, IP: {}'.format(pod_name, capture_file_path, pod_ip))
    result = subprocess.check_output(
        """ tshark -r {} -Y " ip.src == {} && tcp.flags.syn==1 && tcp.flags.ack==0 && not icmp" -Tfields \
          -eip.dst_host  -e tcp.dstport -Eseparator=, | sort --unique """.format(
            capture_file_path, pod_ip), shell=True, timeout=60, stderr=None).decode("utf-8")
    process_stdout_from_process(pod_name, result)


def process_stdout_from_process(pod_name, result):
    if not result or len(result) == 0:
        logging.info("Empty response!")
        return

    target_hosts = result.split("\n")
    for target_host in target_hosts:
        if len(target_host) == 0:
            continue
        parts = target_host.split(",")
        target_ip = parts[0]
        target_port = parts[1]
        logging.debug('IP:{}, Port:{}'.format(target_ip, target_port))
        push_edge_information(pod_name, target_ip, target_port)


@dataclass(frozen=True, eq=True, order=True)
class Pod:
    name: str


def push_edge_information(pod_name, target_ip, target_port):
    print('Source Pod:{}, Destination IP:{}, Destination Port:{}'.format(pod_name, target_ip, target_port))
    if target_ip.startswith('169.254'):
        logging.debug('Skipping ip: {}'.format(target_ip))
        return
    source_pod = Pod(pod_name)
    g.add_vertex(source_pod)
    if not svc_dict.keys().__contains__(target_ip):
        logging.error('No service for IP:{}'.format(target_ip))
    target_pod = find_pod_from_svc(svc_dict[target_ip])
    g.add_vertex(target_pod)
    g.add_edge(source_pod, target_pod)
    # Add port to edge properties


def create_network_policy():
    print("test")


def find_pod_from_svc(svc):
    return find_pod_with_labels(svc["spec"]["selector"])


def find_pod_with_labels(labels: dict):
    for p in pod_dict.values():
        if labels.items() <= dict(p["metadata"]["labels"]).items():
            return Pod(p["metadata"]["name"])
    raise Exception("Could not find pod with labels:{}".format(labels))


def analyze_graph():
    print(g)


def main(argv):
    inputfile = ''
    try:
        inputfile = argv[0]
    except:
        print('5-analyse.py <inputfile>')
        sys.exit(2)
    process_file(inputfile)


if __name__ == '__main__':
    main(sys.argv[1:])
