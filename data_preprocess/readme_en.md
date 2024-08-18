# Data preprocess
This part uses the Allen NLP SRL model. 

The specific model needs to be downloaded and placed in the path: allennlp_model: https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz

More details can be seen: https://demo.allennlp.org/semantic-role-labeling

There are two parts of the data preprocessing：

1. The first part is to convert the original data file into TXT format file in prompt mode by using SRL tool。
2. The second part is to convert the TXT format file into a JSON format file that can be recognized by the model.

The complete command is as follows：
```
PYTHONIOENCODING=UTF-8 nohup python3 preprocess.py \
--convert_type={question_first, question_second, name, explain_relation, relation_explain}
--srl_model={allennlp model path}
--src_data_path={data_dir}
```

The original folder is **data_dir**, which stores **train.txt** and **test.txt**.
Each line of the file has one sample, and the format of each sample is:

> file_name \t du1 \t du2 \t R1 \t R2 \n

For example:
> wsj_2100.pdtb	Couch-potato jocks watching ABC's "Monday Night Football" can now vote during halftime for the greatest play in 20 years from among four or five filmed replays	Two weeks ago, viewers of several NBC daytime consumer segments started calling a 900 number for advice on various life-style issues	Expansion	Conjunction

For convenience, you can directly run the code in run.sh to get the best performance of mode for preprocessing the data.