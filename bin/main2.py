# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot1.3启动文件，添加主动打断功能
'''


import os, time
from core.MyRobert import Bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout_XF import run_tts
from setting import settings
from core.py_sdkXF import XF_text       # 调用讯飞windows-sdk进行语音识别
from core.moni_record_vad import Monitor
import re
import random
from core.unknow_question_save import UnQuetion
from core.face_detcet import FaceRecon
from core import wav2pcm
from classifier.predresult import Predict
from core.utilties import split_words



class FaceDetect(FaceRecon):
    """
    封装人脸识别的类
    """
    @classmethod
    def run(cls):
        return cls('../database/haarcascades/haarcascade_frontalface_alt2.xml')

    def detect(self):
        """
        开启一个线程实时检测画面是否有人脸图像
        :return:
        """
        t = MyThread(self.imag_show)
        t.start()

    @property
    def get_face(self):
        return self.is_face


class XbtBot():
    def __init__(self):
        self.words = None
        self.response = None
        self.results = None
        # self.datadase = None
        self.interflags =False
        self.monitor=Monitor()
        self.face_detect = FaceDetect.run()
        self.face_detect.detect()




    def record_audio(self,isinterrupt=False):
        """
        检测声音，进行录音
        :param isinterrupt:  False 是开启初始对话功能；True 开启机器人主动打断后，对话功能
        :return:
        """
        return self.monitor.run(isinterrupt)



    def voice2word(self):
        """
        语音识别
        :return:
        """
        # start1 = time.time()
        self.words = XF_text(settings.LISTEN_FILE,16000)  # 读取录音文件，通过讯飞sdk实现语音转写
        print("qusetion:%s"%self.words)

    def interrupt(self,response):
        """
        问答分割
        :param response:
        :return:
        """
        self.response1,self.response2 = split_words(response)


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
        print("tulin-{}".format(self.response))

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
            print(self.database )
            #catterbot回答
            chatterbot_respone = self.bot.get_response(self.words)
            if chatterbot_respone != 'False':
                self.response = chatterbot_respone
                print("Mybot-{}".format(self.response))
            else:
                self.tulin_response()
        else:
            self.tulin_response()


    def record(self):
        """
        记录对话信息
        :return:
        """
        s = UnQuetion.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()

    def word2vice(self,response):
        """
        语音合成
        :param response:
        :return:
        """
        run_tts(str(response))

    def search(self,keywords):
        """
        搜索命令关键词
        :param keywords:
        :return:
        """
        results = re.search(keywords, self.words)
        return results

    def inner(self):
        """
        主动打断，开始录音，语音转文字，文字信息判断
        :return:
        """
        #录音
        self.record_audio(isinterrupt=True)
        #检测十秒内是否有声音
        if self.monitor.NoVoiceFlag:
            self.monitor.NoVoiceFlag = False
            self.face_flags = False
        else:
            #检测到声音，语音转文字
            self.voice2word()
            #检索"继续说"等关键词
            continue_results1=self.search(settings.ORDERKEYWORDS)
            #检索"不用说"等关键词
            stop_results2=self.search(settings.ORDERKEYWORDS1)
            if continue_results1:
                #播放后一部分信息
                self.word2vice(self.response2)
            elif stop_results2:
                #播放退出用语
                wav2pcm.audio_play(settings.BYE_TERMS_FILE)
                self.interflags =False
            else:
                #检索到其它非命令性语言，需要继续转化为正常对话
                self.interflags = True

    def talk(self):
        """
        检测到语音信息，开始展开有效问答
        :return:
        """
        #检测words中是否有结束对话命令关键词
        bye_results = self.search(settings.BYEKEYWODS)
        if not bye_results:
            if self.words is not None:
                #开始问答搜素
                self.think()
                if len(str(self.response)) < 30:
                    #语音合成接口
                    self.word2vice(self.response)
                else:
                    self.interrupt(self.response)
                    self.word2vice(self.response1)
                    if self.response2:
                        time.sleep(0.5)
                        #播放打断提示信息
                        wav2pcm.audio_play(settings.INTERRUPT_TERMS_FILE)
                        #主动打断开启
                        self.inner()
            else:
                #播放错误提示信息用语
                wav2pcm.audio_play(settings.SPEACK_TERMS_FILE)
        else:
            #播放退出问答提示信息用语
            wav2pcm.audio_play(settings.BYE_TERMS_FILE)
            # self.face_detect.quit = True

    def run(self):
        """
        开启循环，检测到人脸开始对话机制
        :return:
        """
        while True:
            # try:
                #主动打断对话标志符
                if not self.interflags:
                    # 开启人脸检测功能
                    self.face_flags = self.face_detect.get_face
                    if self.face_flags :
                        #开启录音机功能
                        self.record_audio()
                        #判断10秒内是否检测到声音
                        if self.monitor.NoVoiceFlag:
                            self.monitor.NoVoiceFlag = False
                            self.face_flags =False
                        else:
                            # 语音转文字接口
                            self.voice2word()
                            self.talk()
                else:
                    self.interflags = False
                    self.talk()
            #
            # except:
            #     # 播放错误提示信息用语
            #     wav2pcm.audio_play(settings.LISTEN_TERMS_FILE)


if __name__ == '__main__':
    start = XbtBot()
    start.run()
