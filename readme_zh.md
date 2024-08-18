# Not Just Classification: Recognizing Implicit Discourse Relation on Joint Modeling of Classification and Generation
## 1. 前言
该仓库包含了《Not Just Classification: Recognizing Implicit Discourse Relation on Joint Modeling of Classification and Generation》文章的主要代码，代码使用pytorch框架实现。

论文简介：
![image](cg_t5.jpg)

Implicit discourse relation recognition (IDRR) is a critical task in discourse analysis. Previous studies only regard it as a classification task and lack an in-depth understanding of the semantics of different relations. Therefore, we first view IDRR as a generation task and further propose a method joint modeling of the classification and generation. Specifically, we propose a joint model, CG-T5, to recognize the relation label and generate the target sentence containing the meaning of relations simultaneously. Furthermore, we design three target sentence forms, including the question form, for the generation model to incorporate prior knowledge. To address the issue that large discourse units are hardly embedded into the target sentence, we also propose a target sentence construction mechanism that automatically extracts core sentences from those large discourse units. Experimental results both on Chinese MCDTB and English PDTB datasets show that our model CG-T5 achieves the best performance against several state-of-the-art systems.

论文地址：https://aclanthology.org/2021.emnlp-main.187/

## 2. 具体实现
## 2.1环境安装
python3.6
```bash
conda create -n cg_t5 python=3.6
conda activate cg_t5
```
python依赖库
```bash
pip install -r requirements.txt
```
## 2.2. 数据预处理
原始PDTB 2.0链接：https://catalog.ldc.upenn.edu/LDC2008T05

数据集具体情况，可以参考：https://aclanthology.org/2020.acl-main.480/

数据预处理具体过程，参考data_preprocess文件夹下的readme.md进行处理
## 2.2.  训练和测试过程
我们使用了NVIDIA Tesla V100-SXM2 32G 显卡进行的实验。
尽管我们固定了种子，能够在相同型号的显卡上获得可复现的结果，
但是仍然不能够保证在不同型号的卡上可以得到一样的结果。

T5模型下载后，放置在t5文件夹下：https://huggingface.co/t5-base

训练过程，可以直接运行run_train.sh里的命令

测试过程，可以直接运行run_test.sh里的命令

## 2.3. 评估
评估过程，可以直接运行:
```cmd
python3 evaluate.py
```
 
## 3. 引用及致谢
本文引用格式
```bib
@inproceedings{jiang-etal-2021-just,
    title = "Not Just Classification: Recognizing Implicit Discourse Relation on Joint Modeling of Classification and Generation",
    author = "Jiang, Feng  and
      Fan, Yaxin  and
      Chu, Xiaomin  and
      Li, Peifeng  and
      Zhu, Qiaoming",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.187",
    pages = "2418--2431",
    abstract = "Implicit discourse relation recognition (IDRR) is a critical task in discourse analysis. Previous studies only regard it as a classification task and lack an in-depth understanding of the semantics of different relations. Therefore, we first view IDRR as a generation task and further propose a method joint modeling of the classification and generation. Specifically, we propose a joint model, CG-T5, to recognize the relation label and generate the target sentence containing the meaning of relations simultaneously. Furthermore, we design three target sentence forms, including the question form, for the generation model to incorporate prior knowledge. To address the issue that large discourse units are hardly embedded into the target sentence, we also propose a target sentence construction mechanism that automatically extracts core sentences from those large discourse units. Experimental results both on Chinese MCDTB and English PDTB datasets show that our model CG-T5 achieves the best performance against several state-of-the-art systems.",
}
```

感谢[gpt2生成新闻项目](https://github.com/liucongg/GPT2-NewsTitle)，
[t5-pegasus pytorch项目](https://github.com/renmada/t5-pegasus-pytorch)，
[span-rep项目](https://github.com/shtoshni/span-rep)，
我们的代码基于以上项目得以构建起来，在此表示感谢。

    