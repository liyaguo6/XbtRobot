# -*- coding: utf-8 -*-
'''
@auther: Liyaguo
@summary: 处理机器人逻辑对话信息，一个是来自于本地chatterbot语料库信息检索信息，另一个是来自于tulin外部API接口
'''
import os,sys
from core.record import Record
from core.thd import MyThread
from core.MyRobot import Bot
from core.TuLinRobot import TuLin
from classifier.predresult import Predict



class RobotProces:
    def __init__(self,words):
        self.words =words
        self.response =None

    @property
    def bot(self):
        """
        根据数据库不同，实例化chatterbot对象
        :return:
        """
        obj =  Bot.chattbot(self.database)
        return obj

    def classifiler(self):
        """
        分类器
        :return:
        """
        return Predict(question=self.words).predict()

    def tulin(self):
        """
        开启tulin线程
        :return:
        """
        self.t = MyThread(TuLin, args=(self.words,))
        self.t.setDaemon(True)
        self.t.start()

    def tulin_response(self):
        """
        利用tulin寻找答案
        :return:
        """
        self.t.join()
        self.response = self.t.get_result()
        self.record()

    def think(self):
        """
        问答搜素，tulin+chatterbot数据库
        :return:
        """
        #开启一个图灵线程
        self.tulin()
        #开启分类器
        classifier_result = self.classifiler()
        if classifier_result !=0:
            #chatterbot数据库名称
            self.database = "XbtCorpus%s"%(classifier_result)
            #catterbot回答
            chatterbot_respone = self.bot.get_response(self.words)
            if chatterbot_respone != 'False':
                self.response = str(chatterbot_respone)
            else:
                self.tulin_response()
        else:
            self.tulin_response()

    def record(self):
        """
        记录对话信息
        :return:
        """
        s = Record.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()
