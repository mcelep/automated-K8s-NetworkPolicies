# -*- coding: utf-8 -*-
############################################################
# Author By: Dedi Bar                                      #
# Email: dediba@gmail.com                                  #
# Name: MqttClient.py                                      #
# Python 3.7                                               #
# Version: 1.0.0                                           #
############################################################
import re
import os
import yaml
import pandas as pd
import xlsxwriter
import datetime


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    return (dict2.update(dict1))


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_files_in_directory(directory):
    entries = os.scandir(directory)
    sort_entries = sorted(entries, key=lambda e: e.stat().st_mtime)
    return sort_entries


class K8sParser(object):

    def __init__(self):
        self.conf = {}
        self.sep = os.sep
        self.app_name = "K8sParser"
        self.config_name = "%s%s" % (self.app_name, ".yaml")
        replace = "%s%s%s%s" % (self.sep, 'src', self.sep, os.path.basename(__file__))
        self.home = os.path.abspath(__file__).replace(replace, '')
        self.conf_dir = "%s%s%s" % (self.home, self.sep, "conf")
        self.out_dir = "%s%s%s" % (self.home, self.sep, "out")
        create_directory(self.out_dir)
        self.config_file = "%s%s%s" % (self.conf_dir, self.sep, self.config_name)
        self.config = yaml.load(open(self.config_file, 'r'), Loader=yaml.FullLoader)
        self.files_folder = "%s%s%s" % (self.home, self.sep, self.config.get('files_folder'))

    def parse_file(self, filename):
        graph = {}
        regex_first_junk = "\d{2}[:]\d{2}[:]\d{2}[.]\d+ IP "
        regex_ip = "\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}"
        regex_port = "\d+"
        regex_pod_name = "[\-,\.,a-z,0-9]+"
        regex_direction = "[>|<]"
        regex__ip_pod = "%s|%s" % (regex_ip, regex_pod_name)
        regex_end_junk = ".*"
        regex_row_match = '%s(%s)[.](%s) (%s) (%s)[.](%s):(%s)' % \
                          (regex_first_junk,
                           regex__ip_pod, regex_port,
                           regex_direction,
                           regex__ip_pod, regex_port,
                           regex_end_junk)

        with open(filename) as f:
            for line in f:
                match = re.search(regex_row_match, line)
                if match:
                    if match.group(3) == '>':
                        source_ip = match.group(1)
                        source_port = match.group(2)
                        dest_ip = match.group(4)
                        dest_port = match.group(5)
                    elif match.group(3) == '<':
                        source_ip = match.group(4)
                        source_port = match.group(5)
                        dest_ip = match.group(1)
                        dest_port = match.group(2)
                    else:
                        print("wrong match exit")
                        exit(-1)

                    # Filter connection that one of the ports are in 'ports_filter'
                    if int(source_port) not in self.config.get('ports_filter') and int(dest_port) not in self.config.get('ports_filter'):
                        row = ("%s,%s,%s" % (source_ip, source_port, dest_ip))
                        if row in graph.keys():
                            graph[row]["weight"] = graph[row]["weight"] + 1
                        else:
                            # graph[row] = {"source_ip": source_ip, "source_port": source_port, "dest_ip": dest_ip, "dest_port": dest_port, "weight": 1}
                            graph[row] = {"source_ip": source_ip, "source_port": source_port, "dest_ip": dest_ip, "weight": 1}
            f.close()
            return graph
            ######################################################

    def write_files(self, filename, graph):
        graph_list = []
        NowTime = datetime.datetime.now()
        xls_filename = "%s%s%s%s%s%s" % (self.out_dir, self.sep, filename, "_", NowTime.strftime("%d%m%y%H%M%S"), ".xlsx")
        csv_filename = "%s%s%s%s%s%s" % (self.out_dir, self.sep, filename, "_", NowTime.strftime("%d%m%y%H%M%S"), ".csv")
        for track in graph:
            graph_list.append(graph.get(track))

        df = pd.DataFrame.from_dict(graph_list)
        if self.config.get('xls_export'):
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(xls_filename, engine='xlsxwriter')

            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name='graph')

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()
            print("XlsFile details: %s" % xls_filename)

        if self.config.get('csv_export'):
            df.to_csv(csv_filename, index=False)
            print("Csv File details: %s" % csv_filename)

    def main(self):
        network_graph = {}
        path_list = get_files_in_directory(self.files_folder)
        for entry in path_list:
            print("Parsing => %s", entry.name)
            graph = self.parse_file(entry)
            self.write_files(entry.name, graph)
            network_graph.update(graph)
        self.write_files("network_graph", network_graph)


# ~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~ #
######################################################
if __name__ == '__main__':
    instance = K8sParser()
    instance.main()
######################################################
# ~~~~~~~~~~~~~~~~~~~~~~ DONE ~~~~~~~~~~~~~~~~~~~~~~ #
######################################################
