#!/usr/bin/env python
# encoding: utf-8

class Example:
    def __init__(self):
        self.du1 = ""
        self.du2 = ""
        self.label = ""
        self.label_sentence = ""

    def set_data(self, du1, du2, label, label_sentence):
        self.du1 = du1
        self.du2 = du2
        self.label = label
        self.label_sentence = label_sentence

    def to_string(self):
        result = self.du1 + "\n" + self.label_sentence + "\n" + self.du2 + "\n" + self.label + "\n"
        return result