

from DS.Example import Example
from DS.relation_detail import RelationDetail
from tqdm import tqdm

class Converter:
    def __init__(self, convert_type, convert_srl):
        self.example_list = []
        self.convert_type = convert_type
        self.convert_srl = convert_srl
        self.relation_detail = RelationDetail()

    def get_srl(self, du):
        result = self.convert_srl.convert_du(du)
        return result

    def _get_question_sentence_second(self, label, srl):
        result = ""
        srl = srl.strip()
        if label == 'Concession':  # 当一个论元描述了导致c发生的情况a，而另一个论元否定了c。eg:arg1:此外，在很大程度上，琼斯先生可能已经从球队中得到了他想要的东西，arg2:尽管它一直在输。
            result = 'What part of the event does {} negated?'.format(srl)
        elif label == 'Contrast':  # 对比
            result = "What is the opposite of " + srl + '?'
        elif label == "Cause":  # 当arg2是arg1的原因或者结果是都属于‘Cause’类
            result = "What is the cause or result of " + srl + '?'
        elif label == "Pragmatic cause":  # arg1是一个声明，arg2提供了正当理由
            result = 'What claim does {} provided a justification for?'.format(srl)
        elif label == "Conjunction":  # 补充
            result = 'Do you know what {} is a supplement to?'.format(srl)
        elif label == "Instantiation":  # 举例说明
            result = 'what event {} is an example of?'.format(srl)
        elif label == "Alternative":  # 论元之间是可以互相代替
            result = 'Can you replace' + srl + ' with something else?'
        elif label == "List":  # 列表，arg1,arg2是前面论述中定义的列表成员，并不要求论元之间有关系
            result = "What is the other list member for " + srl + '?'
        elif label == "Restatement":  # 解说 arg1:这种逆转在短期国债中表现得更为明显。arg2:美国国库券利率在上周五一度暴跌0.70个百分点后，昨日又跌回了四分之三
            result = 'What {} explained in detail?'.format(srl)
        elif label == "Asynchronous":  # 表示时间顺序,
            result = "What happened before " + srl + ' ?'
        elif label == "Synchrony":  # 表示时间重叠
            result = "What happened in synchrony with " + srl + '?'
        return result

    def _get_question_sentence_first(self, label, srl):
        result = ""
        srl = srl.strip()
        if label == 'Concession':  # 当一个论元描述了导致c发生的情况a，而另一个论元否定了c。eg:arg1:此外，在很大程度上，琼斯先生可能已经从球队中得到了他想要的东西，arg2:尽管它一直在输。
            result = 'What event negates part of ' + srl + '?'
        elif label == 'Contrast':  # 对比
            result = "What is the opposite of " + srl + '?'
        elif label == "Cause":  # 当arg2是arg1的原因或者结果是都属于‘Cause’类
            result = "What is the cause or result of " + srl + '?'
        elif label == "Pragmatic cause":  # arg1是一个声明，arg2提供了正当理由
            result = 'What is the justification of ' + srl + '?'
        elif label == "Conjunction":  # 补充
            result = 'Is there anything to add about ' + srl + '?'
        elif label == "Instantiation":  # 举例说明
            result = "Can you give me an example of " + srl + '?'
        elif label == "Alternative":  # 论元之间是可以互相代替
            result = 'Can you replace ' + srl + ' with something else?'
        elif label == "List":  # 列表，arg1,arg2是前面论述中定义的列表成员，并不要求论元之间有关系
            result = "What is the other list member for " + srl + '?'
        elif label == "Restatement":  # 解说 arg1:这种逆转在短期国债中表现得更为明显。arg2:美国国库券利率在上周五一度暴跌0.70个百分点后，昨日又跌回了四分之三
            result = 'Can you explain ' + srl + ' in detail?'
        elif label == "Asynchronous":  # 表示时间顺序
            result = "What happened after " + srl + '?'
        elif label == "Synchrony":  # 表示时间重叠
            result = "What happened in synchrony with " + srl + '?'
        return result

    def _get_name_sentence(self, label):
        result = "It's a " + label + " relationship."
        return result

    def _get_relation_explain_sentence(self, label, srl1, srl2):
        result = ""
        srl1 = srl1.strip()
        srl2 = srl2.strip()
        if label == 'Concession':  # 当一个论元描述了导致c发生的情况a，而另一个论元否定了c。eg:arg1:此外，在很大程度上，琼斯先生可能已经从球队中得到了他想要的东西，arg2:尽管它一直在输。
            result = 'It is a Concession relation, because {} negates part of {}.'.format(srl2, srl1)
        elif label == 'Contrast':  # 对比
            result = 'It is a Contrast relation, because {} is the opposite of {}.'.format(srl2, srl1)
        elif label == "Cause":  # 当arg2是arg1的原因或者结果是都属于‘Cause’类
            result = 'It is a Cause relation, because {} is the cause or result of {}.'.format(srl2, srl1)
        elif label == "Pragmatic cause":  # arg1是一个声明，arg2提供了正当理由
            result = 'It is a Pragmatic cause relation, because {} justified {}.'.format(srl2, srl1)
        elif label == "Conjunction":  # 补充
            result = 'It is a Conjunction relation, because {} supplemented {}.'.format(srl2, srl1)
        elif label == "Instantiation":  # 举例说明
            result = 'It is a Instantiation relation, because {} is an example of {}.'.format(srl2, srl1)
        elif label == "Alternative":  # 论元之间是可以互相代替
            result = 'It is a Alternative relation, because {} is alternative for {}.'.format(srl2, srl1)
        elif label == "List":  # 列表，arg1,arg2是前面论述中定义的列表成员，并不要求论元之间有关系
            result = 'It is a List relation, becasue {} and {} are both members of the list defined in the previous discussion.'.format(
                srl1, srl2)
        elif label == "Restatement":  # 解说 arg1:这种逆转在短期国债中表现得更为明显。arg2:美国国库券利率在上周五一度暴跌0.70个百分点后，昨日又跌回了四分之三
            result = 'It is a Restatement relation, because {} explained {} in detail.'.format(srl2, srl1)
        elif label == "Asynchronous":  # 表示时间顺序
            result = 'It is Asynchronous relation, because {} happened after {}.'.format(srl2, srl1)
        elif label == "Synchrony":  # 表示时间重叠
            result = 'It is a Synchrony relation, because {} happened in synchrony with {}.'.format(srl2, srl1)
        return result

    def _get_explain_relation_sentence(self, label, srl1, srl2):
        result = ""
        srl1 = srl1.strip()
        srl2 = srl2.strip()
        if label == 'Concession':  # 当一个论元描述了导致c发生的情况a，而另一个论元否定了c。eg:arg1:此外，在很大程度上，琼斯先生可能已经从球队中得到了他想要的东西，arg2:尽管它一直在输。
            result = 'Since {} negates part of {}, so there is a Concession relation.'.format(srl2, srl1)
        elif label == 'Contrast':  # 对比
            result = 'Since {} is the opposite of {}, so there is a Contrast relation.'.format(srl2, srl1)
        elif label == "Cause":  # 当arg2是arg1的原因或者结果是都属于‘Cause’类
            result = 'Since {} is the cause or result of {}, so there is a Cause relation.'.format(srl2, srl1)
        elif label == "Pragmatic cause":  # arg1是一个声明，arg2提供了正当理由
            result = 'Since {} justified {}, so there is a Pragmatic cause relation.'.format(srl2, srl1)
        elif label == "Conjunction":  # 补充
            result = 'Since {} supplemented {}, so there is a Conjunction relation.'.format(srl2, srl1)
        elif label == "Instantiation":  # 举例说明
            result = 'Since {} is an example of {}, so there is a Instantiation relation.'.format(srl2, srl1)
        elif label == "Alternative":  # 论元之间是可以互相代替
            result = 'Since {} is alternative for {}, so there is a Alternative relation.'.format(srl2, srl1)
        elif label == "List":  # 列表，arg1,arg2是前面论述中定义的列表成员，并不要求论元之间有关系
            result = 'Since {} and {} are both members of the list defined in the previous discussion, so there is a List relation.'.format(
                srl1, srl2)
        elif label == "Restatement":  # 解说 arg1:这种逆转在短期国债中表现得更为明显。arg2:美国国库券利率在上周五一度暴跌0.70个百分点后，昨日又跌回了四分之三
            result = 'Since {} explained {} in detail, so there is a Restatement relation.'.format(srl2, srl1)
        elif label == "Asynchronous":  # 表示时间顺序
            result = 'Since {} happened after {}, so there is a Asynchronous relation.'.format(srl2, srl1)
        elif label == "Synchrony":  # 表示时间重叠
            result = 'Since {} happened in synchrony with {}, so there is a Synchrony relation.'.format(srl2, srl1)
        return result

    def to_lower(self, srl):
        item = srl.split(" ")
        if item[0]=="":
            if item[1].isupper():
                return srl
            else:
                new_srl = []
                new_item = item[1].lower()
                new_srl.append(new_item)
                new_srl.extend(item[2:])
                new_srl = " ".join(new_srl)
                return new_srl
        else:
            return srl

    def post_process(self, srl):
        srl = srl.replace(" ,", ",")
        srl = srl.replace(" \'", "\'")
        srl = srl.replace(" - ", "-")
        srl = srl.replace("$ ", "$")
        srl = srl.replace(" & ", "&")
        srl = srl.replace(" %", "%")
        srl = self.to_lower(srl)
        return srl

    def get_label_sentence(self, label, du1, du2):
        result = ""
        if self.convert_type == "question_first":
            srl1 = self.get_srl(du1).split(".")[0]
            srl1 = self.post_process(srl1)
            result = self._get_question_sentence_first(label, srl1)
        elif self.convert_type == "question_second":
            srl2 = self.get_srl(du2).split(".")[0]
            srl2 = self.post_process(srl2)
            result = self._get_question_sentence_second(label, srl2)
        elif self.convert_type == "name":
            result = self._get_name_sentence(label)
        elif self.convert_type == "relation_explain":
            srl1 = self.get_srl(du1).split(".")[0]
            srl1 = self.post_process(srl1)
            srl2 = self.get_srl(du2).split(".")[0]
            srl2 = self.post_process(srl2)
            result = self._get_relation_explain_sentence(label, srl1, srl2)
        elif self.convert_type == "explain_relation":
            srl1 = self.get_srl(du1).split(".")[0]
            srl1 = self.post_process(srl1)
            srl2 = self.get_srl(du2).split(".")[0]
            srl2 = self.post_process(srl2)
            result = self._get_explain_relation_sentence(label, srl1, srl2)
        return result

    def read_file(self, origin_file):
        with open(origin_file, encoding='utf-8', mode='r') as fr:
            lines = fr.readlines()
            for line in tqdm(lines):
                line = line.strip()
                if line != "":
                    items = line.split("\t")
                    du1 = items[1]
                    du2 = items[2]
                    label = items[-1]
                    if label not in self.relation_detail.relation_dict["small"]:
                        continue
                    relation_sentence = self.get_label_sentence(label, du1, du2)
                    example = Example()
                    example.set_data(du1, du2, label, relation_sentence)
                    self.example_list.append(example)

    def save_file(self, des_file):
        with open(des_file, encoding='utf-8', mode='w') as fw:
            for example in self.example_list:
                fw.write(example.to_string() + "\n")
