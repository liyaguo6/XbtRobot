# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot2.1服务端配置文件信息
'''


import os,sys


BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)


##chatterbot机器人配置文件信息
NAME = "XbtRobot"
Storage_Adapter='chatterbot.storage.MongoDatabaseAdapter'
#本地数据库识别可信度阈值
THRESHOLD = 0.7
Logic_Adapters=[
              {'import_path': "chatterbot.logic.BestMatch"},
                {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',  # LowConfidenceAdapter当高信度响应未知时，返回具有高置信度的默认响应。
                'threshold': THRESHOLD,
                'defa'
                'ult_response': 'False'
                },
          ]
# 这是一个滤波器,它的作用是滤掉重复的回答
Filters = [
              'chatterbot.filters.RepetitiveResponseFilter'
          ]

Input_Adapter = "chatterbot.input.VariableInputTypeAdapter"
Output_Adapter = "chatterbot.output.OutputAdapter"
# 设置你的数据库所在的地址端口号
Database_Uri = "mongodb://localhost:27017/"
READ_ONLY = True

#文本分类特征保存文件
Train_Features_Words_File = os.path.join(BASE_DIR,"classifier\\database\\features\\train_features_words.pkl")
Train_Features_File = os.path.join(BASE_DIR,"classifier\\database\\features\\train_features.pkl")



#图灵API的接口信息
Tulin_API_KEY = "164391ebc59c48a88c7c4cc41682e5a3"




#文本分类器配置参数
STOPWORDS = os.path.join(BASE_DIR,'database\\features\\stop_words.pkl')
TRAIN_FEATURES_WORDS = os.path.join(BASE_DIR,'database\\features\\train_features_words.pkl')
TRAIN_FEATURES = os.path.join(BASE_DIR,'database\\features\\train_features.pkl')

#连接未能回答问题的数据库
IP = '127.0.0.1'
PORT =27017
DB ="unquestion"
TABLE='mtest'


#服务端IP和端口，以及最大开启线程数
SERVER_ADDRESS = ('192.168.1.106',8024)
MAX_NUM_THREADS = 20



