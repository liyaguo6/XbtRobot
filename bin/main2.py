from core import wav2pcm
import os, time
from core.MyRobert import Bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout import tts_main
from setting import settings
from core.sound2wordXF import wordfromS  # 该文档使用讯飞api进行语音识别
import core.moni_record
import re
import random
from core.unknow_question_save import UnQuetion
from core.face_detcet import FaceRecon
from core.utilties import random_start_terms
from classifier.predresult import Predict



class FaceDetect(FaceRecon):

    def detect(self):
        t = MyThread(self.imag_show)
        t.start()

    @property
    def get_face(self):
        return self.is_face





class XbtBot:
    def __init__(self):
        self.words = None
        self.response = None
        self.results = None
        # self.datadase = None
        self.face_detect = FaceDetect('../database/haarcascades/haarcascade_frontalface_alt2.xml')
        self.face_detect.detect()
        self.interrupt = False
        while not self.interrupt:
            self.Flags = self.face_detect.get_face
            # print(self.Flags)
            if self.Flags:
                self.run()
    def voice2word(self):
        core.moni_record.monitor(settings.LISTEN_FILE)
        start1 = time.time()
        self.words = wordfromS(settings.LISTEN_FILE)  # 读取录音文件，通过讯飞API实现语音转写
        stop1 = time.time()
        print("讯飞API:%s" % (stop1 - start1))
    @property
    def bot(self):
        obj =  Bot.chattbot(self.database)
        return obj

    def think(self):
        classifier_result = Predict(question=self.words).predict()
        print(classifier_result)
        t = MyThread(TuLin, args=(self.words,))
        t.setDaemon(True)
        t.start()
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
            t.join()
            self.response = t.get_result()
            self.record()
            print("tulin-{}".format(self.response))

        stop2 = time.time()

    def record(self):
        s = UnQuetion.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()

    def word2vice(self):
        # start3 = time.time()
        tts_main(str(self.response))
        stop3 = time.time()
        wav2pcm.audio_play(settings.SPEACK_FILE)
        # print("语音合成时间%s" % (stop3 - start3))
        # t1 = MyThread(wav2pcm.audio_play, args=(str(settings.SPEACK_FILE),))
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # t1.start()

    @property
    def start_term_path(self):
        return random_start_terms()

    def run(self):
        try:
            t2 = MyThread(wav2pcm.audio_play,args=(self.start_term_path,))
            t2.start()
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
                self.interrupt = True
                self.face_detect.quit = True
        except:
            wav2pcm.audio_play(settings.LISTEN_TERMS_FILE)


if __name__ == '__main__':
    start = XbtBot()
