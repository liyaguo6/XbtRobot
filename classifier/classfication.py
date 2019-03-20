import os
import re
import jieba  #处理中文
import collections
import pickle
import jieba.analyse as analyse
from  process_data import get_data
# jieba.set_dictionary("./dict.txt")


class Train:
    def __init__(self,raw_path,others_path,**kwargs):
        self.features_dim =kwargs.get('features_dim',10000)
        self.data_dict = get_data(raw_path,others_path)
        self.all_words_list =[]
        self.train_data_dict = dict()
        self.train_feature_dict =dict()
        # self.train_class_list=["1","0"]
        self.text_processing()
        # self.train()




    def text_processing(self):
        all_text= ''
        for index,item in self.data_dict.items():
            all_text +=','.join(item)
            class_text= ','.join(item)
            self.train_data_dict[index] = list(jieba.cut(class_text,cut_all=False))
        word_list = list(jieba.cut(all_text, cut_all=False))
        all_words_dict = collections.Counter(word_list)
        self.all_words_list=list(all_words_dict.keys())
        self.feature_words=self.clean_data(self.all_words_list)
        if not os.path.exists('database\\features\\train_features_words.pkl'):
            self.save_feature_words(self.feature_words)

            # #key函数利用词频进行降序排序
            # #方法一：
            # all_words_list=all_words_dict.most_common(1000)
            # all_words_list = list(list(zip(*all_words_list))[0])
            # #方法二：
            # all_words_tuple_list =sorted(all_words_dict.items(),key=lambda f:f[1],reverse=True)
            # self.all_words_list.extend(list(list(zip(*all_words_tuple_list))[0]))

    def clean_data(self,words_list):
        with open('./stop_words.pkl', 'rb') as f:
            stopwords_set = set(pickle.load(f))
        n = 1
        self.cleaned_words=[]
        for t in range(0, len(self.all_words_list), 1):
            if n > self.features_dim:  # feature_words的维度10000
                break
            if not words_list[t].isdigit() and words_list[t] not in stopwords_set and 1 < len(
                    words_list[t]) <= 5 and not re.search('\n\d+|\s|\d\n|[^\u4e00-\u9fff]{1,}',self.all_words_list[t]):
                self.cleaned_words.append(self.all_words_list[t])
                n += 1
        return self.cleaned_words

    def save_feature_words(self,data):
        with open('database\\features\\train_features_words.pkl', 'wb') as f:
            pickle.dump(data, f)

    def features(self,text):
        text_dict = dict(collections.Counter(text))
            ## sklearn特征 list
        features = [text_dict[word] if word in text_dict else 0 for word in self.feature_words]
        return features
    #
    def train(self):

        for index,item in self.train_data_dict.items():
            self.train_feature_dict[index]=self.features(item)
        if not os.path.exists(r'./database\features\train_features.pkl'):
            with open(r'./database\features\train_features.pkl', 'wb') as f:
                pickle.dump(self.train_feature_dict, f)


if __name__ == '__main__':
    t =Train('./database/raw_data.csv','./database/others_data.csv',features_dim=10000)
    t.train()
    # print(t.train_data_dict[0])