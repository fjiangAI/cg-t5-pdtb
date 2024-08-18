

from allennlp.predictors.predictor import Predictor
import nltk
import nltk.data
import re


# 1. 对于可能重复的arg和v,只取跨度最大的
# 2. 对于v,arg0,arg1,arg2的，这种具有多个arg的，按照arg0,v,arg1,arg2,arg3的方式排列
# 3. 先将论元分句，然后，每个句子获得srl，然后以句号相连构成大的论元的srl

class ConvertSrl:
    def __init__(self, srl_model_path):
        """
        处理du的srl_list,抽取最大的。
        :param du:
        """
        self.predictor = Predictor.from_path(srl_model_path, cuda_device=0)  # 加载srl模型
        self.nltk_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    def find_ARG(self,sentence):
        """
        返回所有的arg的表示
        :param sentence:
        :return:
        """
        regex = re.compile('\[ARG\d.*?\]')
        result = re.findall(regex, sentence)
        result_dic = {}
        if result:
            # 处理成字典的形式
            for res_str in result:
                result_dic[res_str[1:5].strip()] = res_str[6:-1].strip()
            return result_dic
        return result_dic

    def is_subspan(self, ARG1_list, ARG2_list):
        """
        判断ARG1_list是够是ARG2_list内部串的一个子串
        :param ARG1_list: ["I'",'interested in just the beginning of story']
        :param ARG2_list: [A menu by phone,you decide , ` I'm interested in just the beginning of story No]
        ARG1_list是ARG2_list的一个子串，吧ARG1_list过滤掉
        :return:
        """
        ARG2_string = ' '.join(ARG2_list)
        for arg1 in ARG1_list:
            if arg1 not in ARG2_string:
                return False
        return True

    def get_max_span_srl(self, new_verb_srl):

        """
        得到所有srl中的最大的
        :param sentence: A menu by phone could let you decide, `I'm interested in just the beginning of story No.
        :return: [['let', {'ARG0': 'A menu by phone', 'ARG1': "you decide , ` I 'm interested in just the beginning of story No"}], ['decide', {'ARG0': 'you', 'ARG1': "I 'm interested in just the beginning of story No"}], ["'m", {'ARG1': 'I', 'ARG2': 'interested in just the beginning of story'}]]
        """
        filtered_verb_srl = []  # 过滤掉最小的srl剩下的srl
        for i in range(len(new_verb_srl)):
            ARGi = [arg for arg in new_verb_srl[i][1].values()]
            FLAG = 0
            for j in range(len(new_verb_srl)):
                if j == i:
                    # 相同的不对比
                    continue
                else:
                    ARGj_list = [arg for arg in new_verb_srl[j][1].values()]
                    if self.is_subspan(ARGi, ARGj_list):
                        # 此时要判断ARGi中所有的arg是否被ARG_list中的所有ARG包含了
                        # 为真，则被包含了，此时break,ARGi不是最大的
                        FLAG = 1  # 表示ARGI不是最大的
                        break
            if FLAG == 0:  # 表示ARGi是最大的
                filtered_verb_srl.append(new_verb_srl[i])
            else:
                FLAG = 0
        return filtered_verb_srl

    def combine_inner_sentencesrl(self, srl_list):
        """
        输入过滤之后的srl_list,其中只包括最大span的srl，相连构成该句子的srl表示
        :param srl_list: [['take', {'ARG0': 'The CFTC', 'ARG1': 'those arguments'}], ['allowing', {'ARG0': 'The CFTC', 'ARG1': 'exceptions to its restrictions'}]]
        :return:
        """
        final_sentence = ''
        i = 0
        for verb, arg_dic in srl_list:
            arg_list = []
            for _, arg_str in arg_dic.items():
                arg_list.append(arg_str)
            arg0 = arg_list[0]
            arg1 = ','.join(arg_list[1:])
            if i == 0:
                final_sentence += arg0 + ' ' + verb + ' ' + arg1
            else:
                final_sentence += ', ' + arg0 + ' ' + verb + ' ' + arg1
            i += 1
        return final_sentence

    def get_du_srl_list(self, du):
        """

        :param du_text:
        :return:
        """
        du_sentences = self.nltk_tokenizer.tokenize(du)
        du_slr_list = []  # 按照句子获得srl
        for sen in du_sentences:
            du_slr_list.append(self.predictor.predict(sentence=sen))
        # 抽取
        return du_sentences, du_slr_list

    def convert_du(self, du):

        """
        :param sentence_list: 分好句的论元['His hands sit farther apart on the keyboard.', 'Seventh chords make you feel as though he may break into a (very slow) improvisatory riff']
        :param sentence_srl_list: 每一个句子对应的allennlp的srl的输出[{'verbs': [{'verb': 'sit', 'description': '[ARG1: His hands] [V: sit] [ARGM-MNR: farther apart] [ARG2: on the keyboard] .', 'tags': ['B-ARG1', 'I-ARG1', 'B-V', 'B-ARGM-MNR', 'I-ARGM-MNR', 'B-ARG2', 'I-ARG2', 'I-ARG2', 'O']}], 'words': ['His', 'hands', 'sit', 'farther', 'apart', 'on', 'the', 'keyboard', '.']}, {'verbs': [{'verb': 'make', 'description': '[ARG0: Seventh chords] [V: make] [ARG1: you feel as though he may break into a ( very slow ) improvisatory riff]', 'tags': ['B-ARG0', 'I-ARG0', 'B-V', 'B-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1']}, {'verb': 'feel', 'description': 'Seventh chords make [ARG0: you] [V: feel] [ARG1: as though he may break into a ( very slow ) improvisatory riff]', 'tags': ['O', 'O', 'O', 'B-ARG0', 'B-V', 'B-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1']}, {'verb': 'may', 'description': 'Seventh chords make you feel as though he [V: may] break into a ( very slow ) improvisatory riff', 'tags': ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-V', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']}, {'verb': 'break', 'description': 'Seventh chords make you feel as though [ARG0: he] [ARGM-MOD: may] [V: break] [ARG1: into a ( very slow ) improvisatory riff]', 'tags': ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-ARG0', 'B-ARGM-MOD', 'B-V', 'B-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1']}], 'words': ['Seventh', 'chords', 'make', 'you', 'feel', 'as', 'though', 'he', 'may', 'break', 'into', 'a', '(', 'very', 'slow', ')', 'improvisatory', 'riff']}]
        :return:
        """
        final_du = ''  # 一个篇章单元的srl，句内的以逗号隔开，句间以句号隔开，其中都以arg0 v arg1,arg2的形式连接
        sentence_list, sentence_srl_list = self.get_du_srl_list(du)
        for sentence, sentence_srl in zip(sentence_list, sentence_srl_list):
            sentence_verbs_list = sentence_srl['verbs']
            new_verb_verb_srl = []  # 索引0为verb，1为srl_dic
            for verb_dic in sentence_verbs_list:
                verb_word = verb_dic['verb']
                verb_depsciption = verb_dic['description']
                # 过滤掉不含有ARG的条目，以及ARG数量为1的条目，只保留存在arg0,arg1，arg2,等等的条目
                arg_list = self.find_ARG(verb_depsciption)  # 找到verb
                if len(arg_list) == 0 or len(arg_list) == 1:
                    continue
                else:
                    new_verb_verb_srl.append([verb_word, arg_list])
            # 从一个句子内的所有srl中得到最大的srl
            filtered_verb_srl = self.get_max_span_srl(new_verb_verb_srl)
            if len(filtered_verb_srl) == 0:  # 没有srl，则返回整个句子
                final_du += ' ' + sentence + '. '
            else:
                inner_sentence = self.combine_inner_sentencesrl(filtered_verb_srl)
                final_du += ' ' + inner_sentence + '. '
        return final_du

