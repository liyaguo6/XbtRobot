# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: 分类器预测
'''

import jieba
import pickle
from sklearn.naive_bayes import MultinomialNB  # 多项式分类
import collections
from setting import settings
import logging
jieba.setLogLevel(logging.INFO)

class Predict:
    def __init__(self,**kwargs):

        with open(settings.Train_Features_Words_File , 'rb') as f:
            self.features_words = pickle.load(f)
        with open(settings.Train_Features_File, 'rb') as f:
            self.train_features_dict= pickle.load(f)
        self.train_features_class =list(self.train_features_dict.keys())
        self.train_features = list(self.train_features_dict.values())
        self.predict_features = self.features(kwargs.get('question'))

    def features(self,text):
        text_words_list = list(jieba.cut(text, cut_all=True))
        text_words_dict = dict(collections.Counter(text_words_list))
        predict_features=[[text_words_dict[word] if word in text_words_dict else 0 for word in self.features_words]]
        return predict_features



    def predict(self):
        clf=MultinomialNB()
        clf = clf.fit(self.train_features, self.train_features_class)
        result = clf.predict(self.predict_features)[0]
        return result

if __name__ == '__main__':
    p = Predict(question='滁州市人民政府外事办公室的咨询电话是什么')
    print(p.predict())