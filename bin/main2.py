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
import threading
import pyaudio
import wave


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
        self.last_answer = None
        self.last_que = None
        self.eve = threading.Event()
        self.eve1 = threading.Event()
        self.xlock = threading.Lock()
        self.flag = 0
        with self.xlock:
            self.eve.clear()
            self.eve1.set()
            self.flag = 0
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
        obj = Bot.chattbot(self.database)
        return obj

    def think(self):
        classifier_result = Predict(question=self.words).predict()
        print(classifier_result)
        t = MyThread(TuLin, args=(self.words,))
        t.setDaemon(True)
        t.start()
        if classifier_result != 0:
            self.database = "XbtCorpus%s" % (classifier_result)
            print(self.database)
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
        else:
            t.join()
            self.response = t.get_result()
            self.record()
            print("tulin-{}".format(self.response))

        # stop2 = time.time()

    def record(self):
        s = UnQuetion.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()

    def word2vice(self):
        # start3 = time.time()
        tts_main(str(self.response))
        # stop3 = time.time()
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # print("语音合成时间%s" % (stop3 - start3))
        t = MyThread(wav2pcm.audio_play, args=(str(settings.SPEACK_FILE),))
        t.setDaemon(True)
        t.start()
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # t1.start()

    @property
    def start_term_path(self):
        return random_start_terms()

    def audio_play_1(self, filename):
        CHUNK = 1024
        p = pyaudio.PyAudio()
        wf = wave.open(filename, 'rb')

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(CHUNK)
        while len(data) > 0:
            if self.flag == 1:
                break
            self.eve.wait()
            data = wf.readframes(CHUNK)
            stream.write(data)
        # stop
        with self.xlock:
            self.eve.clear()
            self.eve1.set()
            self.flag = 0
        stream.stop_stream()
        stream.close()

    def word2vice_tmp(self):

        tts_main(str(self.response))

        with self.xlock:
            self.eve.set()
            self.eve1.clear()

        t = MyThread(self.audio_play_1, args=(settings.SPEACK_FILE,))

        t.setDaemon(True)
        t.start()

    def end_do(self):
        with self.xlock:
            self.flag = 1
            self.eve.clear()
            self.eve1.set()

    def run(self):
        try:
            if self.eve1.is_set() and not self.eve.is_set():
                t2 = MyThread(wav2pcm.audio_play, args=(self.start_term_path,))
                t2.start()

            self.voice2word()
            #self.words = input(("Enter your message >> "))

            tmp = re.sub("[！，。？、~,]", "", self.words)
            self.words=tmp

            self.results = re.findall(r'(再见|goodbye|bye bye|拜拜|退出|再会|待会见)', self.words)
            # last_answer=""
            if len(self.results) == 0:

                if self.words is not None:

                    if (self.words in ['你不要说了', '好了好了', '我不想听了', '别说了']) and not self.eve1.is_set():
                        self.end_do()
                    elif not self.eve.is_set() and self.eve1.is_set():
                        if ('再说一遍' in self.words or '重复一遍' in self.words or '再说一次' in self.words or '重复一下' in self.words )and self.last_answer is not None:
                            self.response = self.last_answer
                            print(self.response)
                        else:
                            self.think()
                        self.word2vice_tmp()
                        self.last_answer = self.response
                        self.last_que = self.words

                else:
                    wav2pcm.audio_play(settings.SPEACK_TERMS_FILE)
            else:
                self.end_do()
                wav2pcm.audio_play(settings.BYE_TERMS_FILE)
                self.interrupt = True
                self.face_detect.quit = True


        except:
            wav2pcm.audio_play(settings.LISTEN_TERMS_FILE)


if __name__ == '__main__':
    start = XbtBot()
