# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: xbtrobot2.1 封装人脸检测、客户端通信
'''


import os, time,sys

from core.thd import MyThread
from core.TuLinRobert import TuLin
from core.speakout_XF import run_tts
from settings import setting
from core.py_sdkXF import XF_text       # 调用讯飞windows-sdk进行语音识别
from core.moni_record_vad import Monitor  #调用录影机API
import re
import random

from core.face_detcet import FaceRecon
from core import wav2pcm
from core.utilties import split_words
from core.client import Client



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


class RobotClient(Client):
    def __init__(self,server_address,connect=True):
        super().__init__(server_address)

    @classmethod
    def start(cls):
        obj = cls(setting.SERVER_ADDRESS)
        return obj


class XbtBot():
    def __init__(self):
        self.words = None
        self.response = None
        self.results = None
        self.client = RobotClient.start()
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
        self.words = XF_text(setting.LISTEN_FILE,16000)  # 读取录音文件，通过讯飞sdk实现语音转写
        print("qusetion:%s"%self.words)

    def interrupt(self,response):
        """
        问答分割
        :param response:
        :return:
        """
        self.response1,self.response2 = split_words(response)



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
            continue_results1=self.search(setting.ORDERKEYWORDS)
            #检索"不用说"等关键词
            stop_results2=self.search(setting.ORDERKEYWORDS1)
            if continue_results1:
                #播放后一部分信息
                self.word2vice(self.response2)
            elif stop_results2:
                #播放退出用语
                wav2pcm.audio_play(setting.BYE_TERMS_FILE)
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
        bye_results = self.search(setting.BYEKEYWODS)
        if not bye_results:
            if self.words is not None:
                #开始问答搜素
                self.response=self.client.send_recv(self.words)
                print(self.response)
                if len(str(self.response)) < 30:
                    #语音合成接口
                    self.word2vice(self.response)
                else:
                    self.interrupt(self.response)
                    self.word2vice(self.response1)
                    if self.response2:
                        time.sleep(0.5)
                        #播放打断提示信息
                        wav2pcm.audio_play(setting.INTERRUPT_TERMS_FILE)
                        #主动打断开启
                        self.inner()
            else:
                #播放错误提示信息用语
                wav2pcm.audio_play(setting.SPEACK_TERMS_FILE)
        else:
            #播放退出问答提示信息用语
            wav2pcm.audio_play(setting.BYE_TERMS_FILE)
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
