#!/usr/bin/env python
# encoding: utf-8

import argparse
import os
import random
import sys

sys.path.append("../")
from data_preprocess.convert_data import Converter
from data_preprocess.convert_srl import ConvertSrl
from data_preprocess.custom_data import DataConverter
import numpy as np
import torch

def seed_everything(seed=1029):
    '''
    设置整个开发环境的seed
    :param seed:
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

def make_dir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' create success!')
    else:
        print(path + ' exists.')
    return path


def set_args():
    """设置训练模型所需参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--srl_model', default='./allennlp_model/structured-prediction-srl-bert.2020.12.15.tar.gz',
                        type=str, help='srl模型路径')
    parser.add_argument('--src_data_path', default='../data_dir/', type=str, help='数据源文件路径')
    return parser.parse_args()


if __name__ == '__main__':
    seed_everything(seed=42)
    args = set_args()
    convert_srl = ConvertSrl('./allennlp_model/structured-prediction-srl-bert.2020.12.15.tar.gz')
    print("加载srl模型成功")
    for convert_type in ["question_first"]:
        des_data_path = "../data_dir/" + convert_type + "/"
        make_dir(des_data_path)
        for dataset_type in ["train", "test"]:
            print("convert_type")
            converter = Converter(convert_type=convert_type, convert_srl=convert_srl)
            converter.read_file(origin_file=args.src_data_path + "/" + dataset_type + ".txt")
            converter.save_file(des_file=des_data_path + "/" + dataset_type + ".txt")
            data_converter = DataConverter()
            data_converter.read_file(source_file=des_data_path + "/" + dataset_type + ".txt")
            data_converter.write_file(des_file=des_data_path + "/" + dataset_type + ".json")
