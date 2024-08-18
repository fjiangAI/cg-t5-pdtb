#!/usr/bin/env python
# encoding: utf-8

import json

class DataConverter:
    def __init__(self):
        self.data_list = []
        self.static_list=[]
    def read_file(self, source_file):
        with open(source_file, encoding='utf-8', mode='r') as fr:
            line = fr.read()
            line.strip("\n\n")
            items = line.split("\n\n")
            for num, item in enumerate(items):
                d = {}
                line_item = item.split("\n")
                if len(line_item)!=4:
                    continue
                d["du1"] = line_item[0]
                d["rs"] = line_item[1]
                d["du2"] = line_item[2]
                d["label"] = line_item[3]
                self.data_list.append(d)
                self.static_list.append(len(d["rs"]))
    def write_file(self, des_file):
        with open(des_file, encoding='utf-8', mode="w") as fw:
            fw.write(json.dumps(self.data_list, ensure_ascii=False))
