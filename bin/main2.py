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
        # self.VoiceFlag = False


    def record_audio(self):  # 检测声音，进行录音
        return self.monitor.run()



    def voice2word(self):
        # start1 = time.time()
        self.words = XF_text(settings.LISTEN_FILE,16000)  # 读取录音文件，通过讯飞sdk实现语音转写
        print("response:%s"%self.words)

        # stop1 = time.time()
        # print("语音识别时间:%s" % (stop1 - start1))

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


    def record(self):
        s = UnQuetion.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()

    def word2vice(self):
        start3 = time.time()
        run_tts(str(self.response))
        stop3 = time.time()
        print("语音合成时间+播放：%s" % (stop3 - start3))
        # t1 = MyThread(wav2pcm.audio_play, args=(str(settings.SPEACK_FILE),))
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # t1.start()






    def run(self):
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
                        self.results = re.findall(r'(再见|goodbye|bye bye|拜拜|退出|再会|待会见)', self.words)
                        if len(self.results) == 0:
                            if self.words is not None:
                                self.think()
                                self.word2vice()
                                # else:
                                #     tts_main("好的，一会聊",settings.SPEACK_FILE)
                                #     wav2pcm.audio_play(settings.SPEACK_FILE)
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
