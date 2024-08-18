#!/usr/bin/env python
# encoding: utf-8

class RelationDetail:
    def __init__(self):
        self.relation_dict = {
            "small": [
                'Concession', 'Contrast',
                'Cause', 'Pragmatic cause',
                'Conjunction', 'Instantiation', 'Alternative', 'List', 'Restatement',
                'Asynchronous', 'Synchrony'
            ],
            "big": ["Comparison",
                    "Contingency",
                    "Expansion",
                    "Temporal"]
        }

        self.relation2big_dict = {'Concession': 'Comparison',
                                  'Contrast': 'Comparison',
                                  'Cause': 'Contingency',
                                  'Pragmatic cause': 'Contingency',
                                  'Conjunction': 'Expansion',
                                  'Instantiation': 'Expansion',
                                  'Alternative': 'Expansion',
                                  'List': 'Expansion',
                                  'Restatement': 'Expansion',
                                  'Asynchronous': 'Temporal',
                                  'Synchrony': 'Temporal'}

        self.question2relation_first_dict = {
            "What event negates part of": 'Concession',
            "What is the opposite of": 'Contrast',
            "What is the cause or result of": 'Cause',
            'What is the justification of': 'Pragmatic cause',
            'Is there anything to add about': 'Conjunction',
            "Can you give me an example of": 'Instantiation',
            'Can you replace': 'Alternative',
            "What is the other list member for": 'List',
            'Can you explain': 'Restatement',
            "What happened after": 'Asynchronous',
            "What happened in synchrony with": 'Synchrony'
        }

        self.question2relation_second_dict = {
            "What part of the event does": 'Concession',
            "What is the opposite of": 'Contrast',
            "What is the cause or result": 'Cause',
            'provided a justification for': 'Pragmatic cause',
            'is a supplement to': 'Conjunction',
            "is an example of": 'Instantiation',
            'Can you replace': 'Alternative',
            "What is the other list member for": 'List',
            'explained in detail': 'Restatement',
            "What happened before": 'Asynchronous',
            "What happened in synchrony with": 'Synchrony'
        }
        self.name2relation_dict = {
            'Concession': 'Concession',
            'Contrast': 'Contrast',
            'Cause': 'Cause',
            'Pragmatic cause': 'Pragmatic cause',
            'Conjunction': 'Conjunction',
            'Instantiation': 'Instantiation',
            'Alternative': 'Alternative',
            'List': 'List',
            'Restatement': 'Restatement',
            'Asynchronous': 'Asynchronous',
            'Synchrony': 'Synchrony'
        }
