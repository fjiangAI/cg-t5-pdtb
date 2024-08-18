#!/usr/bin/env python
# encoding: utf-8


from sklearn.metrics import classification_report

from DS.relation_detail import RelationDetail


class Reporter:
    def __init__(self, type="small"):
        self.relation_detail = RelationDetail()
        self.y_true = []
        self.y_pred = []
        self.type = type
        self.relation_list = self.relation_detail.relation_dict[type]

    def detail(self, y_true, y_pred):
        self.y_true = self.convert(y_true)
        self.y_pred = self.convert(y_pred)
        result = classification_report(self.y_true, self.y_pred, target_names=self.relation_list, digits=4)
        return result

    def convert(self, ys):
        new_ys = []
        for y in ys:
            if y == "Unknown":
                if self.type == "small":
                    y = "Cause"
                elif self.type == "big":
                    y = "Contingency"
            new_ys.append(self.relation_list.index(y))
        return new_ys


def read_file(src_file, type="small", class_type="generate"):
    y_true = []
    y_pred = []
    with open(src_file, encoding='utf-8', mode='r') as fr:
        lines = fr.readlines()
        for num, line in enumerate(lines):
            line = line.strip()
            items = line.split("\t")
            if type == "small":
                y_true.append(items[4])
                if class_type == "generate":
                    y_pred.append(items[-4])
                else:
                    y_pred.append(items[-2])
            elif type == "big":
                y_true.append(items[5])
                if class_type == "generate":
                    y_pred.append(items[-3])
                else:
                    y_pred.append(items[-1])
    return y_true, y_pred


if __name__ == '__main__':
    src_files = ["question_first"]
    types = ["small", "big"]
    class_types = ["generate", "class"]
    for src_file in src_files:
        for class_type in class_types:
            for type in types:
                print(src_file + "\t" + class_type + "\t" + type)
                y_true, y_pred = read_file(src_file="result_detail_" + src_file + "_endpoint1111.txt", type=type,
                                           class_type=class_type)
                reporter = Reporter(type=type)
                result = reporter.detail(y_true, y_pred)
                print(result)
