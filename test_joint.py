#!/usr/bin/env python
# encoding: utf-8

import json
import random
import numpy as np
import torch
import os
import argparse

from torch.nn.utils.rnn import pad_sequence

import sys

sys.path.append("../")

from transformers.models.t5.tokenization_t5 import T5Tokenizer
from DS.relation_detail import RelationDetail


class Converter:
    def __init__(self, convert_type):
        self.relation_detail = RelationDetail()
        self.relation_big_dict = self.relation_detail.relation2big_dict
        if convert_type == "name":
            self.relation_dict = self.relation_detail.name2relation_dict
        elif convert_type == "question_first":
            self.relation_dict = self.relation_detail.question2relation_first_dict
        elif convert_type == "question_second":
            self.relation_dict = self.relation_detail.question2relation_second_dict
        elif convert_type == "explain_relation":
            self.relation_dict = self.relation_detail.name2relation_dict
        elif convert_type == "relation_explain":
            self.relation_dict = self.relation_detail.name2relation_dict
    def convert_line(self, line):
        for key in self.relation_dict.keys():
            if key in line:
                return self.relation_dict[key] + "\t" + self.relation_big_dict[self.relation_dict[key]]
        return "Unknown\tUnknown"

    def convert_lines(self, lines):
        results = []
        for line in lines:
            result = self.convert_line(line)
            results.append(result)
        return results


def set_args():
    """设置模型预测所需参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default='0', type=str, help='设置预测时使用的显卡,使用CPU设置成-1即可')
    parser.add_argument('--model_path', default='output_dir/model-9', type=str, help='模型文件路径')
    parser.add_argument('--vocab_path', default='t5/', type=str, help='词表')
    parser.add_argument('--test_file', default='./data_dir/test.json', type=str, help='词表')
    parser.add_argument('--generate_max_len', default=200, type=int, help='生成的最大长度')
    parser.add_argument('--max_len', type=int, default=512, help='输入模型的最大长度，要比config中n_ctx小')
    parser.add_argument('--seed', type=int, default=42, help='随机种子')
    parser.add_argument('--des_file', default='result.txt', type=str, help='预测结果')
    parser.add_argument('--batch_size', default=8, type=int, help='一次预测出几个例子')
    parser.add_argument('--convert_type', default="name", type=str, help='预测类型')
    return parser.parse_args()


def save_file(des_file, du1, du2, real_rs, rs, class_name, big_class_name, convert_type):
    converter = Converter(convert_type)
    with open(des_file, encoding='utf-8', mode="a") as fw:
        fw.write(du1 + "\t" + du2 + "\t" + real_rs + "\t" + rs + "\t" +
                 converter.convert_line(real_rs) + "\t" + converter.convert_line(
            rs) + "\t" + class_name + "\t" + big_class_name + "\n")


def save_files(des_file, du1_list, du2_list, real_rs_list, rs_list, class_list, big_class_list,convert_type):
    for i in range(len(du1_list)):
        save_file(des_file, du1_list[i], du2_list[i], real_rs_list[i], rs_list[i], class_list[i], big_class_list[i],convert_type)


def generate_results(output, tokenizer):
    title_list = []
    for i in range(len(output)):
        title = tokenizer.decode(output[i][1:], skip_special_tokens=True)
        title_list.append(title)
    return title_list


def generate_class_name(class_output):
    class_list = []
    big_class_list = []
    relation_detail = RelationDetail()
    relation_big_dict = relation_detail.relation2big_dict
    relation_list = relation_detail.relation_dict["small"]

    for i in range(len(class_output)):
        class_name = relation_list[class_output[i]]
        big_class_name = relation_big_dict[class_name]
        class_list.append(class_name)
        big_class_list.append(big_class_name)
    return class_list, big_class_list


def seed_everything(seed=1029):
    '''
    设置整个开发环境的seed
    :param seed:
    :param device:
    :return:
    '''
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # some cudnn methods can be random even after fixing the seed
    # unless you tell it to be deterministic
    torch.backends.cudnn.deterministic = True


def main():
    """主函数"""
    # 设置预测的配置参数
    args = set_args()
    # 获取设备信息
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICE"] = args.device
    device = torch.device("cuda" if torch.cuda.is_available() and int(args.device) >= 0 else "cpu")
    if args.seed:
        seed_everything(seed=args.seed)
    # 实例化tokenizer和model
    tokenizer = T5Tokenizer.from_pretrained(args.vocab_path)
    model = torch.load(args.model_path)
    model.to(device)
    model.eval()
    rs_max_len = args.generate_max_len
    max_len = args.max_len
    src_file = args.test_file
    des_file = args.des_file
    samples = get_samples(src_file=src_file)
    input_list = []
    du1_list = []
    du2_list = []
    real_rs_list = []
    rs_list = []
    for num, sample in enumerate(samples):
        if sample["label"] == "None":
            continue
        input_ids = convert_feature(sample, tokenizer, rs_max_len, max_len)
        input_list.append(torch.tensor(input_ids, dtype=torch.long))
        du1_list.append(sample["du1"])
        du2_list.append(sample["du2"])
        real_rs_list.append(sample["rs"])
        if len(input_list) < args.batch_size:
            continue
        input_list = pad_sequence(input_list, batch_first=True, padding_value=0)
        input_tensors = torch.tensor(input_list).long().to(device)
        text_output, class_output = model.generate(input_tensors,
                                                   decoder_start_token_id=1,
                                                   eos_token_id=1,
                                                   max_length=args.generate_max_len)
        rs_list = generate_results(text_output, tokenizer)
        class_list, big_class_list = generate_class_name(class_output)
        save_files(des_file=des_file, du1_list=du1_list, du2_list=du2_list, real_rs_list=real_rs_list,
                   rs_list=rs_list, class_list=class_list, big_class_list=big_class_list, convert_type=args.convert_type)
        input_list = []
        du1_list = []
        du2_list = []
        real_rs_list = []
        rs_list = []
    input_list = pad_sequence(input_list, batch_first=True, padding_value=0)
    input_tensors = torch.tensor(input_list).long().to(device)
    text_output, class_output = model.generate(input_tensors,
                                               max_length=args.generate_max_len)
    rs_list = generate_results(text_output, tokenizer)
    class_list, big_class_list = generate_class_name(class_output)
    save_files(des_file=des_file, du1_list=du1_list, du2_list=du2_list, real_rs_list=real_rs_list,
               rs_list=rs_list, class_list=class_list, big_class_list=big_class_list, convert_type=args.convert_type)


def convert_feature(sample, tokenizer, rs_max_len, max_len):
    """
        数据处理函数
        Args:
            sample: 一个字典，格式为{"du1": du1, "du2": du2}

        Returns:

        """
    input_ids = []
    # 对正文进行tokenizer.tokenize分词
    du1_tokens = tokenizer.tokenize(sample["du1"])
    du2_tokens = tokenizer.tokenize(sample["du2"])
    # 判断如果正文过长，进行截断
    while len(du1_tokens) + len(du2_tokens) > max_len - rs_max_len - 3:

        if len(du1_tokens) > len(du2_tokens):
            du1_tokens = du1_tokens[:-1]
        else:
            du2_tokens = du2_tokens[:-1]
    # 生成模型所需的input_ids和token_type_ids
    input_ids.extend(tokenizer.convert_tokens_to_ids(du1_tokens))
    input_ids.append(2)
    input_ids.extend(tokenizer.convert_tokens_to_ids(du2_tokens))
    input_ids.append(2)
    # 判断input_ids长度是否小于等于最大长度
    assert len(input_ids) <= max_len
    return input_ids


def get_samples(src_file):
    with open(src_file, encoding='utf-8', mode='r') as fr:
        samples = json.load(fr)
    return samples


if __name__ == '__main__':
    main()
