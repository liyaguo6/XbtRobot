from core import wav2pcm
import os, time
from core.MyRobert import Bot, MyThread
from core.TuLinRobert import TuLin
from core.moni_record import monitor
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
        self.con_words= None
        self.eve = threading.Event()
        self.eve1 = threading.Event()
        self.xlock = threading.Lock()
        self.eve_con=threading.Event()
        self.flag = 0
        with self.xlock:
            self.eve.clear()
            self.eve_con.clear()
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
        tmp1 = wordfromS(settings.LISTEN_FILE)  # 读取录音文件，通过讯飞API实现语音转写
        tmp = re.sub("[！，。？、~,]", "", tmp1)
        print(tmp)
        if not self.eve.is_set() and not self.eve1.is_set():
            res = re.findall(r'(接着说|继续说|说吧)', tmp)
            if(len(res)<=0):
                self.end_do()
            else:
                self.eve_con.set()
                self.eve.set()
        else:
            self.words=tmp
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
        time_start=time.time()
        have=0
        while len(data) > 0:
            if self.flag == 1:
                break
            self.eve.wait()
            data = wf.readframes(CHUNK)
            stream.write(data)
            time_now = time.time()
            if (time_now - time_start > 8 and have==0):
                have=1
                with self.xlock:
                    self.eve.clear()
                    self.eve1.clear()
                    self.eve_con.clear()
                time.sleep(0.2)
                wav2pcm.audio_play(settings.CONTINUE_TERMS_FILE)

               # self.voice2word()
               # self.words = input(("请问我可以继续说嘛 "))
                self.eve_con.wait()

                # if self.con_words == '不用了':#打算
                #     break
                # else:
                #     with self.xlock:
                #         self.eve.set()
                #         self.eve1.clear()
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
           # self.words = input(("Enter your message >> "))
            self.results = re.findall(r'(再见|goodbye|bye bye|拜拜|退出|再会|待会见)', self.words)
            # last_answer=""
            if len(self.results) == 0:

                if self.words is not None:
                    if (len(re.findall(r'(不要说了|好了好了|好啦好啦|别说了|不想听了|停下来)',self.words))>0) and not self.eve1.is_set():
                        self.end_do()
                        time.sleep(0.3)
                    elif not self.eve.is_set() and self.eve1.is_set():
                        if (len(re.findall(r'(再说一遍|重复一遍|再说一次|我没听清楚)', self.words)) > 0)and self.last_answer is not None:
                            self.response = self.last_answer
                            print(self.response)
                        else:
                           # self.response='在拥有亚当斯、维埃拉的时代，阿森纳曾经有过充满男人血性的时候，并且也创造过辉煌。但是随着球队风格越来越技术流，加上主帅温格的性格使然，号称“枪手”的阿森纳，却逐渐丧失了血性，在面对曼联、切尔西、利物浦，甚至一些英超中下游踢法强硬的球队时，经常会被欺负。这种欺负不是技战术方面的问题，往往都是在硬度、精气神上被对方碾压，并且最终导致某场比赛比分上、某项赛事争夺上的失利。'
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
