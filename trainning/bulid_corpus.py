# -*- coding: utf-8 -*-
'''
@auther: liya guo
@summary: 利用chatterbot框架训练机器人
'''
from chatterbot.trainers import ChatterBotCorpusTrainer
import os,sys,re,time
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# corpus_file = os.path.join(BASE_DIR,"database/jsonfile/test.json")
corpus_file = os.path.join(BASE_DIR,'trainning\\test2.json')
# from core.MyRobert import bot

from chatterbot import ChatBot


# bot = ChatBot("Terminal",
#               storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
#               logic_adapters=[
#                   {'import_path': "chatterbot.logic.BestMatch"},
#               ],
#               filters=[
#                   'chatterbot.filters.RepetitiveResponseFilter'
#               ],
#               # trainer='chatterbot.trainers.ListTrainer',
#               input_adapter="chatterbot.input.VariableInputTypeAdapter",
#               output_adapter="chatterbot.output.OutputAdapter",
#               database_uri="mongodb://localhost:27017/",
#               database="xbttest2",
#               read_only=True,
#               # trainer='chatterbot.trainers.ListTrainer'
#               )
# bot.set_trainer(ChatterBotCorpusTrainer)



# 使用中文语料库训练它
# if __name__ == '__main__':
#     bot.train([
#         "这是医院领导来视察。",
#         "欢迎领导莅临指导",
#         "这是指南针科创园的马总",
#             "领导辛苦了",
#     ])
import json
import pandas as pd
# f.write(json.dumps(data_dict))
# data_dict = dict(conversations=list1)
#使用csv文件导入
def load_file(path,save_path='test_file.json',mode="txt"):
    list1 = []
    if mode == 'txt':
        with open(path,'r',encoding='utf-8') as h:
            lines = h.readlines()
            for line in lines:
                if line != "\n" :
                    line_list =line.replace('\n','').split(' ')
                    list1.append(line_list)
    else:
        df = pd.read_csv(path,header=None,encoding='gbk')
        for index in range(df.shape[0]):
            sample=list(df.loc[index,:].dropna())
            # sample.append(sample.pop(1))
            list1.append(sample[:2])
            print("################")
    data_dict = dict(conversations=list1)
    with open(save_path,'w',encoding='utf-8') as fj:
        fj.write(json.dumps(data_dict))



databases=['XbtCorpus1','XbtCorpus2','XbtCorpus3','XbtCorpus4','XbtCorpus5']

class TrainCroups():

    def __init__(self,path,name,save_path='test_file.json',mode="txt",**kwargs):
        self.path =path
        self.save_path =save_path
        self.mode = mode
        self.data_list=list()
        self.data_dict =dict()
        self.database = None
        self.json_file_path = None
        self.kwargs =kwargs
        if self.mode == 'txt':
            self._read_txt()
        if self.mode == 'csv':
            self._read_csv()
        self._write_json_file()
        # self.train(self.json_file_path)

    def _read_txt(self):
        with open(self.path,'r',encoding='utf-8') as h:
            lines = h.readlines()
            for line in lines:
                if line != "\n" :
                    line_list =line.replace('\n','').split(' ')
                    self.data_list.append(line_list)
    def _read_csv(self):
        df = pd.read_csv(self.path, header=0, encoding='gbk',usecols=['labels','origques','answer'])
        for index1,db in enumerate(databases):
            temp_list=[]
            for index2,rows in df[df['labels']==index1+1].iterrows():
                # sample = list(df.loc[index, :].dropna())
                if len(rows['answer']) <=300:
                    temp_list.append([rows['origques'],rows['answer']])
            print('%s save %s sapmles '%(db,len(temp_list)))
            self.data_dict[db] =temp_list
            print("################")


    def _write_json_file(self):
        for key,item in self.data_dict.items():
            with open('./croups/%s.json'%(key), 'w', encoding='utf-8') as fj:
                fj.write(json.dumps(dict(conversations=item)))



if __name__ == '__main__':
    # load_file("./cropus_test.txt",save_path='cropus_test.json',mode='txt')
    # bot.train("./cropus_test.json")
    t=TrainCroups(path=r'./gover2.csv',name='Myrobot',mode='csv',
              )
    kwargs ={'storage_adapter':'chatterbot.storage.MongoDatabaseAdapter',
            'logic_adapters' :[
                                   {'import_path': "chatterbot.logic.BestMatch"},
                                           ],
            'filters' :['chatterbot.filters.RepetitiveResponseFilter' ],
             'input_adapter' :"chatterbot.input.VariableInputTypeAdapter",
            'output_adapter' : "chatterbot.output.OutputAdapter",
            'database_uri' :"mongodb://localhost:27017/",
            'read_only' : True,
        }
    dirs = os.listdir('./croups')
    for i in dirs:
        database,_=re.split('\.',i)
        kwargs['database'] = database
        bot = ChatBot('XbtRobot',**kwargs)
        bot.set_trainer(ChatterBotCorpusTrainer)
        bot.train('./croups/%s.json'%(database))


    # t.start_train()

    # bot.train("./my_export.json")
    # bot.train(ret)
    # start = time.time()
    # response = bot.get_response("有没有档案资料来馆查阅服务的监督电话")
    # print(response)
    # end = time.time()
    # print(end-start)
    # load_csv_file('gover.csv','gover.json',mode='csv')
    # bot.train("./gover.json")
    # pass