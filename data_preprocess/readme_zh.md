# 数据预处理
该部分使用到了AllenNLP的SRL模块，具体模型需要下载后放在allennlp_model下：https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz

详情参见：https://demo.allennlp.org/semantic-role-labeling

数据预处理主要分为2个部分：

1. 第一个部分为将原始数据利用SRL工具转换为提示模式的txt格式文件。
2. 第二部分则将文件转换为模型部分可以读取的json格式文件。

完整运行代码如下：
```
PYTHONIOENCODING=UTF-8 nohup python3 preprocess.py \
--convert_type={question_first, question_second, name, explain_relation, relation_explain}
--srl_model={allennlp model path}
--src_data_path={data_dir}
```

原始文件夹为data_dir，里面存放train.txt和test.txt文件。
文件每行一个样例，每个样例的格式为：

> file_name \t du1 \t du2 \t R1 \t R2 \n

例如：
> wsj_2100.pdtb	Couch-potato jocks watching ABC's "Monday Night Football" can now vote during halftime for the greatest play in 20 years from among four or five filmed replays	Two weeks ago, viewers of several NBC daytime consumer segments started calling a 900 number for advice on various life-style issues	Expansion	Conjunction

方便起见，可以直接参考run.sh里的代码运行，获得最好性能的预处理后的结果。