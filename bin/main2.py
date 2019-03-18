# -*- coding:utf-8 -*-
from core import wav2pcm
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
import threading
from classifier.predresult import Predict
import shutil



class FaceDetect(FaceRecon):

    def detect(self):
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
        self.Flags = False
        self.monitor=Monitor()
        self.face_detect = FaceDetect('../database/haarcascades/haarcascade_frontalface_alt2.xml')
        self.face_detect.detect()
        self.eve_con = threading.Event()
        self.xlock=threading.Lock()
        self.resp_next = None
        self.have=0
        self.speaking=0
        # self.VoiceFlag = False


    def record_audio(self):  # 检测声音，进行录音
        return self.monitor.run(self.have)



    def voice2word(self):

        tmp1 = XF_text(settings.LISTEN_FILE,16000)  # 读取录音文件，通过讯飞sdk实现语音转写
        tmp = re.sub("[！，。？、~,]", "", tmp1)
        if self.have == 1:
            if self.speaking == 0:
                print ('//////////////////////////////////////////////////////')
                res = re.findall(r'(接着说|继续说)', tmp)
                if(len(res)<=0):
                    self.end_do()
                else:
                    with self.xlock:
                        self.eve_con.set()
                        self.speaking = 1
        else:
            self.words=tmp


    @property
    def bot(self):
        obj =  Bot.chattbot(self.database)
        return obj

    def classifiler(self):
        return Predict(question=self.words).predict()

    def tulin(self):
        self.t = MyThread(TuLin, args=(self.words,))
        self.t.setDaemon(True)
        self.t.start()

    def tulin_response(self):
        self.t.join()
        self.response = self.t.get_result()
        self.record()
        print("tulin-{}".format(self.response))

    def think(self):
        self.tulin()
        classifier_result = self.classifiler()
        print(classifier_result)

        if classifier_result !=0:
            self.database = "XbtCorpus%s"%(classifier_result)
            print(self.database )
            chatterbot_respone = self.bot.get_response(self.words)
            response = chatterbot_respone
            print(response)
            if response != 'False':
                self.response = response
                print("Mybot-{}".format(self.response))
            else:
                self.tulin_response()
        else:
            self.tulin_response()

    def end_do(self):
        with self.xlock:
            self.have = 0
            self.speaking = 0
            self.resp_next = None



    def record(self):
        s = UnQuetion.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()

    def word2vice(self):
        start3 = time.time()
        if(len(self.response)>settings.long_limit):
            t=len(self.response)
            for index,uchar in enumerate(self.response):
                if (uchar=='。' or uchar =='.') and index > settings.first_len:
                    t=index
                    break
            resp1=self.response[0:t]
            self.resp_next=self.response[t+1:]

            run_tts(resp1)
            with self.xlock:
                self.eve_con.clear()
                self.speaking=0

            run_tts('请问还需要我继续说嘛')
            self.eve_con.wait() # 暂停
            run_tts(self.resp_next)
        else:
             run_tts(str(self.response))
        self.end_do()
        stop3 = time.time()
        print("语音合成时间+播放：%s" % (stop3 - start3))

        # t1 = MyThread(wav2pcm.audio_play, args=(str(settings.SPEACK_FILE),))
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # t1.start()

    def run(self):
        with self.xlock:
            self.have=0
            self.speaking=0
            self.eve_con.set()
        while True:
            # try:
                # 开启人脸检测功能
                self.Flags = self.face_detect.get_face
                if self.Flags :
                    self.record_audio()
                    if self.monitor.VoiceFlag:
                        self.monitor.VoiceFlag = False
                        self.Flags =False
                    else:
                        self.voice2word()
                        #self.words = input(("Enter your message >> "))
                        self.results = re.findall(r'(再见|goodbye|bye bye|拜拜|退出|再会|待会见)', self.words)
                        if len(self.results) == 0:

                            if  self.have==1 :
                                continue

                            if self.words is not None:
                                #self.think()
                                self.response = '在拥有亚当斯、维埃拉的时代，阿森纳曾经有过充满血性的时候，并且也创造过辉煌。但是随着球队风格越来越技术流，加上主帅温格的性格使然，号称“枪手”的阿森纳，却逐渐丧失了血性，在面对曼联、利物浦，甚至一些英超中下游踢法强硬的球队时，经常会被欺负。这种欺负不是技战术方面的问题，往往都是在硬度、精气神上被对方碾压，并且最终导致某场比赛比分上、某项赛事争夺上的失利。'
                                with self.xlock:
                                    self.have = 1
                                    self.speaking=1
                                    self.eve_con.set()
                                t=MyThread(self.word2vice,)
                                t.setDaemon(True)
                                t.start()
                                 # self.word2vice()
                            else:
                                wav2pcm.audio_play(settings.SPEACK_TERMS_FILE)
                        else:
                            wav2pcm.audio_play(settings.BYE_TERMS_FILE)
                            self.face_detect.quit = True

            # except:
            #     wav2pcm.audio_play(settings.LISTEN_TERMS_FILE)


if __name__ == '__main__':
    start = XbtBot()
    start.run()
